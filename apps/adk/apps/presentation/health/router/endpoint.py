# presentation/health/health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.applications.health.services.health_check import HealthService
from apps.domain.health.health_state import HealthStatus
from apps.infrastructure._database.config.postgres import get_db
from apps.infrastructure.health.health_repository import DatabaseHealthRepository

router = APIRouter()
service = HealthService(DatabaseHealthRepository())


# /api/v1/health
@router.get("")
async def liveness():
    return {"status": "ok"}


# /api/v1/health/ready
@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    status = await service.check_db(db)

    if status is HealthStatus.DOWN:
        raise HTTPException(status_code=503, detail="Database not ready")

    return {"status": HealthStatus.OK}
