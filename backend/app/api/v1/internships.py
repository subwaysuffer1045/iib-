from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.database import get_db
from app.services.filter_service import get_filtered_internships
from app.models.internship import Internship
from app.models.company import Company
from app.schemas.internship import InternshipCardSchema, InternshipDetailSchema
from sqlalchemy import select, and_

router = APIRouter()

@router.get("", response_model=dict)
async def list_internships(
    region: str = Query(..., description="Region code e.g. mumbai, bengaluru, remote, all-india"),
    domain: str = Query(..., description="Domain slug is required for discovery"),
    work_mode: Optional[str] = Query(None),
    freshness: Optional[str] = Query(None),
    verified_only: bool = Query(False),
    high_trust: bool = Query(False),
    sort: str = Query("newest"),
    limit: int = Query(20, le=50),
    cursor: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    List internships for a specific domain and region.
    Public access - no authentication required.
    """
    result = await get_filtered_internships(
        db=db,
        region=region,
        domain=domain,
        work_mode=work_mode,
        freshness=freshness,
        verified_only=verified_only,
        high_trust=high_trust,
        sort=sort,
        cursor=cursor,
        limit=limit,
    )
    
    # Serialize using flattened schema
    internships_data = []
    for row in result["data"]:
        internship, company = row
        internships_data.append(
            InternshipCardSchema(
                id=internship.id,
                slug=internship.slug,
                title=internship.title,
                company_name=company.name,
                company_trust_score=company.trust_score,
                city=internship.city,
                state=internship.state,
                location_text=internship.location_text,
                work_mode=internship.work_mode.value,
                domain_slug=internship.domain_slug,
                stipend_min=internship.stipend_min,
                stipend_max=internship.stipend_max,
                stipend_text=internship.stipend_text,
                apply_by=internship.apply_by,
                is_expiring_soon=internship.is_expiring_soon,
                trust_score=internship.trust_score,
                verification_status=internship.verification_status.value,
                duration_text=internship.duration_text,
                freshness_bucket=internship.freshness_bucket.value if internship.freshness_bucket else None,
                skills=internship.skills or [],
                posted_at=internship.posted_at,
            )
        )
    
    return {
        "success": True,
        "data": internships_data,
        "meta": result["meta"],
    }

@router.get("/{slug}")
async def get_internship(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get detailed internship information.
    Public access - no authentication required.
    """
    result = await db.execute(
        select(Internship, Company)
        .join(Company, Internship.company_id == Company.id)
        .where(Internship.slug == slug, Internship.is_public == True)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Internship not found")
    
    internship, company = row
    
    return {
        "success": True,
        "data": InternshipDetailSchema(
            id=internship.id,
            slug=internship.slug,
            title=internship.title,
            description_raw=internship.description_raw,
            company_id=company.id,
            company_name=company.name,
            company_trust_score=company.trust_score,
            city=internship.city,
            state=internship.state,
            work_mode=internship.work_mode.value,
            stipend_min=internship.stipend_min,
            stipend_max=internship.stipend_max,
            stipend_text=internship.stipend_text,
            apply_url=internship.apply_url,
            apply_by=internship.apply_by,
            trust_score=internship.trust_score,
            verification_status=internship.verification_status.value,
            domain_slug=internship.domain_slug,
            duration_text=internship.duration_text,
            skills=internship.skills or [],
            posted_at=internship.posted_at,
        )
    }
