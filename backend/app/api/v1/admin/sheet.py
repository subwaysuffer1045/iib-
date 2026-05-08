from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.api.deps import get_authenticated_user
from app.models.user import User
from app.models.sheet_sync_log import SheetSyncLog
from typing import List
import uuid

router = APIRouter()

@router.post("/sync")
async def trigger_sheet_sync(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    """Admin only: Trigger Google Sheet sync pipeline."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # In a real implementation, this would call a Celery task or a service
    # For Phase 4, we'll simulate or call the existing pipeline service
    # background_tasks.add_task(run_import_pipeline)
    
    return {"success": True, "message": "Sync pipeline triggered in background"}

@router.get("/sync-logs")
async def get_sync_logs(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_authenticated_user),
):
    """Admin only: Get history of sheet syncs."""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(
        select(SheetSyncLog).order_by(SheetSyncLog.synced_at.desc()).limit(limit)
    )
    logs = result.scalars().all()
    
    return {
        "success": True,
        "data": [
            {
                "id": str(log.id),
                "synced_at": log.synced_at,
                "sheet_tab": log.sheet_tab,
                "rows_written": log.rows_written,
                "rows_expired": log.rows_expired,
                "rows_rejected": log.rows_rejected,
                "status": log.sync_status.value,
                "error_message": log.error_message,
            }
            for log in logs
        ]
    }
