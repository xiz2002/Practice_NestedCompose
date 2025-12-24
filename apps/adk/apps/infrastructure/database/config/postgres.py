# infrastructure/database/config/postgres.py
from __future__ import annotations

from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

class PostgresSettings(BaseSettings):
    """
    Docker 환경변수로부터 Postgres 접속 정보를 읽어옵니다.

    예)
      POSTGRES_HOST=postgres
      POSTGRES_PORT=5432
      POSTGRES_DB=devdb
      POSTGRES_USER=devuser
      POSTGRES_PASSWORD=devpassword
    """

    model_config = SettingsConfigDict(
        env_file=".env",  # 선택: 로컬 개발 시 .env도 읽고 싶으면 유지
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = Field(..., alias="POSTGRES_HOST")
    port: int = Field(5432, alias="POSTGRES_PORT")
    db: str = Field(..., alias="POSTGRES_DB")
    user: str = Field(..., alias="POSTGRES_USER")
    password: SecretStr = Field(..., alias="POSTGRES_PASSWORD")

    # 선택 옵션들
    driver: Literal["asyncpg", "psycopg"] = Field("asyncpg", alias="POSTGRES_DRIVER")
    sslmode: str | None = Field(None, alias="POSTGRES_SSLMODE")
    application_name: str | None = Field(None, alias="POSTGRES_APP_NAME")
    
    # Suppress mypy warning
    schema: str = Field("public", alias="POSTGRES_SCHEMA") # ignore

@lru_cache
def get_postgres_settings() -> PostgresSettings:
    """
    Settings는 프로세스 생애주기 동안 거의 변하지 않으므로 캐싱하는 패턴을 권장합니다.
    """
    return PostgresSettings()  # type: ignore


def build_postgres_dsn(settings: PostgresSettings | None = None) -> str:
    """
    Postgres DSN(SQLAlchemy URL)을 생성합니다.

    asyncpg 예)
      postgresql+asyncpg://user:pass@host:5432/dbname

    psycopg(Async) 예)
      postgresql+psycopg://user:pass@host:5432/dbname
    """
    s = settings or get_postgres_settings()

    # SecretStr은 get_secret_value()로 꺼내야 합니다.
    pwd = s.password.get_secret_value()

    if s.driver == "asyncpg":
        scheme = "postgresql+asyncpg"
    else:
        scheme = "postgresql+psycopg"

    dsn = f"{scheme}://{s.user}:{pwd}@{s.host}:{s.port}/{s.db}"

    # 쿼리 파라미터(선택)
    params: list[str] = []
    if s.sslmode:
        params.append(f"sslmode={s.sslmode}")
    if s.application_name:
        params.append(f"application_name={s.application_name}")

    if params:
        dsn = f"{dsn}?{'&'.join(params)}"

    return dsn


def build_postgres_dsn_sync(settings: PostgresSettings | None = None) -> str:
    """
    동기용 Postgres DSN(SQLAlchemy URL)을 생성합니다.
    """
    return build_postgres_dsn(settings).replace("+asyncpg", "")


@lru_cache
def get_async_engine() -> AsyncEngine:
    """
    Async SQLAlchemy 엔진을 생성합니다.
    """
    dsn = build_postgres_dsn()
    return create_async_engine(
        dsn,
        pool_pre_ping=True,
        # echo=True,  # 필요 시 SQL 로그
    )


@lru_cache
def get_async_sessionmaker() -> async_sessionmaker:
    """
    FastAPI Depends 등에서 재사용할 수 있는 AsyncSession factory.
    """
    engine = get_async_engine()
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
        autocommit=False,
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    AsyncSessionLocal = get_async_sessionmaker()
    async with AsyncSessionLocal() as session:
        yield session
