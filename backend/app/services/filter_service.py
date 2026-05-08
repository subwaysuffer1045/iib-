from typing import Optional, Any
from sqlalchemy import select, and_, or_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.internship import Internship, WorkMode, FreshnessBucket
from app.models.company import Company, VerificationStatus
from app.utils.india_regions import REGION_TO_CITIES, REMOTE_REGION_VALUE, ALL_INDIA_VALUE

async def get_filtered_internships(
    db: AsyncSession,
    region: str,
    domain: Optional[str] = None,
    work_mode: Optional[str] = None,
    freshness: Optional[str] = None,
    verified_only: bool = False,
    high_trust: bool = False,
    sort: str = "newest",
    cursor: Optional[str] = None,
    limit: int = 20,
) -> dict:
    """Build and execute internship filter query."""
    
    # Base: only public active internships
    conditions: list[Any] = [
        Internship.is_public == True,
        Internship.is_active == True,
    ]
    
    # Region filter
    if region == REMOTE_REGION_VALUE:
        conditions.append(Internship.work_mode == WorkMode.remote)
    elif region != ALL_INDIA_VALUE:
        cities = REGION_TO_CITIES.get(region, [])
        if cities:
            conditions.append(or_(*[Internship.city == city for city in cities]))
    
    # Domain filter
    if domain:
        conditions.append(Internship.domain_slug == domain)
    
    # Work mode filter (secondary, can override region)
    if work_mode and region != REMOTE_REGION_VALUE:
        conditions.append(Internship.work_mode == WorkMode(work_mode))
    
    # Freshness filter
    if freshness:
        conditions.append(Internship.freshness_bucket == FreshnessBucket(freshness))
    
    # Quality filters
    if verified_only:
        conditions.append(Internship.verification_status == VerificationStatus.verified)
    
    if high_trust:
        conditions.append(Internship.trust_score >= 75)
    
    # Build query
    query = (
        select(Internship, Company)
        .join(Company, Internship.company_id == Company.id)
        .where(and_(*conditions))
    )
    
    # Sort
    if sort == "newest":
        query = query.order_by(Internship.posted_at.desc().nullslast(), Internship.created_at.desc())
    elif sort == "stipend":
        query = query.order_by(Internship.stipend_min.desc().nullslast())
    elif sort == "deadline":
        query = query.order_by(Internship.apply_by.asc().nullslast())
    elif sort == "trust":
        query = query.order_by(Internship.trust_score.desc())
    else:
        query = query.order_by(Internship.created_at.desc())
    
    query = query.limit(limit + 1)
    
    result = await db.execute(query)
    rows = result.all()
    
    has_more = len(rows) > limit
    if has_more:
        rows = rows[:limit]
    
    return {
        "data": rows,
        "meta": {
            "total": len(rows),
            "has_more": has_more,
            "cursor": None,
        }
    }
