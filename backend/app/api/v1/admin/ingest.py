from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings
from typing import Optional, List, Dict, Any
from app.models.company import Company, VerificationStatus
from app.models.internship import Internship, InternshipStatus, WorkMode, InternshipSource, StipendConfidence, ApplyLinkType
from app.utils.slug import make_slug, make_company_slug
from sqlalchemy import select
from datetime import datetime, date, timezone
from urllib.parse import urlparse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

def utcnow_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)

async def verify_ingest_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate bulk ingestion via API key or admin user session.
    """
    if credentials:
        if credentials.credentials == settings.IIB_INGEST_API_KEY:
            return True
            
        # Fallback to normal user auth
        from app.services.auth_service import get_current_user
        try:
            user = await get_current_user(credentials.credentials, db)
            if user and user.role.value == "admin":
                return True
        except Exception:
            pass
            
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized ingestion access"
    )

@router.post("")
async def bulk_ingest_internships(
    payload: Dict[str, List[Dict[str, Any]]],
    db: AsyncSession = Depends(get_db),
    authenticated: bool = Depends(verify_ingest_auth)
):
    """
    Admin only or API Key: Bulk ingest/upsert scraped internships.
    """
    items = payload.get("items", [])
    if not items:
        return {"success": True, "count": 0, "message": "No items provided"}
        
    ingested_count = 0
    now = utcnow_naive()
    
    for item in items:
        try:
            company_name = item.get("company_name", "Unknown").strip()
            title = item.get("title", "").strip()
            apply_link = item.get("apply_link", "").strip()
            domain = item.get("domain", "Web Development")
            
            if not company_name or not title or not apply_link:
                logger.warning(f"Skipping invalid item: {item}")
                continue
                
            # Parse domain from apply link to use as company domain if not present
            parsed_url = urlparse(apply_link)
            domain_name = parsed_url.netloc.lower().replace("www.", "") if parsed_url.netloc else None
            
            # Exclude job board domains from being associated as company domains
            JOB_BOARD_DOMAINS = {
                "internshala.com", "naukri.com", "adzuna.com", "workindia.in", 
                "foundit.in", "foundit.com", "indeed.com", "linkedin.com", 
                "google.com", "glassdoor.com", "ambitionbox.com"
            }
            if domain_name in JOB_BOARD_DOMAINS:
                domain_name = None
            
            # 1. Search for existing Company
            company = None
            if domain_name:
                company_res = await db.execute(
                    select(Company).where(Company.domain == domain_name)
                )
                company = company_res.scalar_one_or_none()
                
            if not company:
                # Search by canonical_name or name match
                canonical_name = company_name.lower().replace(" ", "-")
                company_res = await db.execute(
                    select(Company).where(
                        (Company.canonical_name == canonical_name) | 
                        (Company.name == company_name)
                    )
                )
                company = company_res.scalar_one_or_none()
                
            if not company:
                # Generate unique slug for Company
                slug = make_company_slug(company_name)
                slug_res = await db.execute(select(Company).where(Company.slug == slug))
                if slug_res.scalar_one_or_none():
                    slug = f"{slug}-{str(uuid.uuid4())[:8]}"

                # Create a new Company
                company = Company(
                    id=uuid.uuid4(),
                    name=company_name,
                    canonical_name=company_name.lower().replace(" ", "-"),
                    slug=slug,
                    domain=domain_name,
                    website=f"https://{domain_name}" if domain_name else None,
                    verification_status=VerificationStatus.needs_review,
                    trust_score=45,  # initial trust score
                    created_at=now,
                    updated_at=now
                )
                db.add(company)
                await db.flush() # Ensure ID is populated
                
            # 2. Check if Internship already exists (deduplicate by apply_link or title+company+domain)
            internship = None
            internship_res = await db.execute(
                select(Internship).where(
                    (Internship.apply_link == apply_link) | 
                    ((Internship.title == title) & (Internship.company_id == company.id) & (Internship.domain == domain))
                )
            )
            internship = internship_res.scalar_one_or_none()
            
            # Map work_mode string to Enum
            wm_str = item.get("work_mode", "onsite")
            try:
                work_mode_enum = WorkMode(wm_str)
            except ValueError:
                work_mode_enum = WorkMode.onsite
                
            # Map source string to Enum
            src_str = item.get("source", "manual")
            try:
                source_enum = InternshipSource(src_str)
            except ValueError:
                source_enum = InternshipSource.manual
                
            # Parse last date
            last_date_val = None
            ld_str = item.get("last_date")
            if ld_str:
                try:
                    last_date_val = date.fromisoformat(ld_str)
                except ValueError:
                    pass
                    
            # Parse status
            status_str = item.get("status", "draft")
            try:
                status_enum = InternshipStatus(status_str)
            except ValueError:
                status_enum = InternshipStatus.draft

            is_active_flag = (status_enum == InternshipStatus.active)
            paid_gate_flag = is_active_flag or (float(item.get("stipend_min", 0) or 0) > 0)
            apply_link_valid_flag = is_active_flag

            if internship:
                # Update existing internship
                internship.stipend_min = item.get("stipend_min", internship.stipend_min)
                internship.stipend_text = item.get("stipend_text", internship.stipend_text)
                internship.work_mode = work_mode_enum
                internship.location_text = item.get("location_text", internship.location_text)
                internship.duration_text = item.get("duration_text", internship.duration_text)
                internship.last_date = last_date_val or internship.last_date
                internship.status = status_enum
                internship.is_active = is_active_flag
                internship.is_public = is_active_flag
                internship.paid_gate_passed = paid_gate_flag
                internship.apply_link_valid = apply_link_valid_flag
                if is_active_flag:
                    internship.apply_link_checked_at = now
                internship.updated_at = now
            else:
                # Create a new Internship
                internship = Internship(
                    id=uuid.uuid4(),
                    title=title,
                    slug=make_slug(f"{title}-{company_name}"),
                    company_id=company.id,
                    stipend_min=item.get("stipend_min", 0),
                    stipend_text=item.get("stipend_text", ""),
                    is_paid=float(item.get("stipend_min", 0) or 0) > 0,
                    work_mode=work_mode_enum,
                    location_text=item.get("location_text", "Remote"),
                    duration_text=item.get("duration_text", "Not mentioned"),
                    apply_link=apply_link,
                    apply_url=apply_link,
                    domain=domain,
                    last_date=last_date_val,
                    status=status_enum,
                    source=source_enum,
                    ambitionbox_url=item.get("ambitionbox_url"),
                    glassdoor_url=item.get("glassdoor_url"),
                    is_active=is_active_flag,
                    is_public=is_active_flag,
                    paid_gate_passed=paid_gate_flag,
                    apply_link_valid=apply_link_valid_flag,
                    apply_link_checked_at=now if is_active_flag else None,
                    created_at=now,
                    updated_at=now
                )
                db.add(internship)
                
            await db.commit()
            ingested_count += 1
        except Exception as e:
            logger.error(f"Error ingesting item {item}: {str(e)}")
            await db.rollback()
            continue
            
    return {"success": True, "count": ingested_count, "message": f"Successfully ingested {ingested_count} items"}
