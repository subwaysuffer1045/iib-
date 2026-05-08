from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database import get_db
from app.models.company import Company
import uuid

router = APIRouter()

@router.get("/{company_id}")
async def get_company(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get basic company information."""
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {
        "success": True,
        "data": {
            "id": company.id,
            "name": company.name,
            "website": company.website,
            "trust_score": company.trust_score,
            "verification_status": company.verification_status.value,
        }
    }

@router.get("/{company_id}/verification-summary")
async def get_company_verification_summary(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get insights from the verification process for a company."""
    result = await db.execute(select(Company).where(and_(Company.id == company_id)))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # In a real app, this might pull from a VerificationReport model
    # For now, we return summary from company metadata or hardcoded logic
    return {
        "success": True,
        "data": {
            "trust_score": company.trust_score,
            "verification_status": company.verification_status.value,
            "checks": [
                {"name": "Domain Verification", "status": "passed" if company.trust_score > 50 else "pending"},
                {"name": "Scam Detection", "status": "passed" if company.trust_score > 30 else "flagged"},
                {"name": "Manual Review", "status": "completed" if company.verification_status.value == "verified" else "pending"},
            ]
        }
    }
