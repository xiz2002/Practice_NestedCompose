# infrastructure/database/health_repository.py
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseHealthRepository:
    async def check_alive(self, session: AsyncSession) -> bool:
        try:
            await session.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
