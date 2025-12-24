from sqlalchemy.ext.asyncio import AsyncSession

from apps.domain.health.health_state import HealthStatus
from apps.infrastructure.database.health_repository import (
    DatabaseHealthRepository,
)


class HealthService:
    def __init__(self, repo: DatabaseHealthRepository):
        self._repo = repo

    async def check_db(self, session: AsyncSession) -> HealthStatus:
        if await self._repo.check_alive(session):
            return HealthStatus.OK
        return HealthStatus.DOWN
