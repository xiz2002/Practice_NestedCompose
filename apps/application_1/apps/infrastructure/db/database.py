# infrastructure/database.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import text

DATABASE_URL = (
    "postgresql+asyncpg://devuser:devpassword@postgres:5432/devdb"
)

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 중요: 죽은 커넥션 자동 감지
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def check_connection(session) -> bool:
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
