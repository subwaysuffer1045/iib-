from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from app.database import get_db
from app.api.deps import get_authenticated_user
from app.models.user import User
from app.models.company import Company, VerificationStatus
from app.schemas.admin import CompanyVerifySchema, CompanyOverrideScoreSchema
import uuid

router = APIRouter()

@router.post("/{company_id}/verify")
async def verify_company(
    company_id: uuid.UUID,
    data: CompanyVerifySchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    """Admin only: Verify a company."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company.verification_status = VerificationStatus(data.status)
    # Add logic for notes if needed
    
    await db.commit()
    return {"success": True, "message": f"Company status updated to {data.status}"}

@router.post("/{company_id}/reject")
async def reject_company(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    """Admin only: Reject a company."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company.verification_status = VerificationStatus.rejected
    await db.commit()
    return {"success": True, "message": "Company rejected"}

@router.patch("/{company_id}/override-score")
async def override_company_score(
    company_id: uuid.UUID,
    data: CompanyOverrideScoreSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    """Admin only: Override company trust score."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company.trust_score = data.trust_score
    # In production, log the reason
    
    await db.commit()
    return {"success": True, "new_score": company.trust_score}
