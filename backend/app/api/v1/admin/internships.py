from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database import get_db
from app.api.deps import get_authenticated_user
from app.models.user import User
from app.models.internship import Internship
from app.pipelines.validation.paid_gate import PaidGate
from app.pipelines.validation.link_validator import LinkValidator
import uuid

router = APIRouter()

@router.post("/{internship_id}/approve")
async def approve_internship(
    internship_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    """
    Admin only: Approve an internship for public listing.
    Runs Paid Gate and Link Validator before approval.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(select(Internship).where(Internship.id == internship_id))
    internship = result.scalar_one_or_none()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
    
    # 1. Paid Gate
    paid_gate = PaidGate()
    # Convert model to dict for check method
    internship_data = {
        "stipend_min": internship.stipend_min,
        "stipend_confidence": internship.stipend_confidence,
    }
    if not paid_gate.check(internship_data):
        raise HTTPException(
            status_code=400, 
            detail=f"Failed Paid Gate: Stipend ({internship.stipend_min}) is invalid or low confidence."
        )
    
    # 2. Link Validator
    link_validator = LinkValidator()
    if not internship.apply_url:
        raise HTTPException(status_code=400, detail="Internship is missing application URL")
        
    is_valid, link_type, error_msg = await link_validator.validate(internship.apply_url)
    if not is_valid:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed Link Validation: {error_msg or 'Link is unreachable'}"
        )
    
    # 3. Approve
    internship.is_public = True
    internship.is_active = True
    # If the company was rejected, we might not want to approve its internships?
    # For now, we assume if admin clicks approve, they mean it.
    
    await db.commit()
    return {
        "success": True, 
        "message": "Internship approved and is now public",
        "link_type": link_type
    }
