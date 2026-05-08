from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.redis_client import get_redis

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    redis_status = "ok"
    
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
    
    try:
        r = get_redis()
        await r.ping()
        await r.aclose()
    except Exception:
        redis_status = "error"
    
    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "db": db_status,
        "redis": redis_status,
        "version": "1.0.0"
    }
