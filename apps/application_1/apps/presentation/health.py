from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from apps.infrastructure.db.database import get_db, check_connection


router = APIRouter()

# interfaces/api/v1/health
@router.get("/health")
async def liveness():
    return {"status": "ok"}

# interfaces/api/v1/health/ready
@router.get("/health/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    ok = await check_connection(db)
    if not ok:
        raise HTTPException(status_code=503, detail="Database not ready")

    return {"status": "ready"}