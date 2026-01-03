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
    db_schema: str = Field("public", alias="POSTGRES_SCHEMA")


@lru_cache
def get_postgres_settings() -> PostgresSettings:
    """
    Settings는 프로세스 생애주기 동안 거의 변하지 않으므로 캐싱하는 패턴을 권장합니다.
    """
    return PostgresSettings()  # type: ignore


def _build_query_params(settings: PostgresSettings) -> str:
    """
    드라이버 공통으로 URL에 붙여도 되는(혹은 SQLAlchemy가 이해하는) 것만 구성.
    """
    params: list[str] = []

    if settings.sslmode:
        params.append(f"sslmode={settings.sslmode}")
    if settings.application_name:
        params.append(f"application_name={settings.application_name}")

    return "&".join(params)


def build_postgres_dsn(settings: PostgresSettings | None = None) -> str:
    """
    Postgres DSN(SQLAlchemy URL)을 생성합니다.

    asyncpg 예)
      postgresql+asyncpg://user:pass@host:5432/dbname
    """
    s = settings or get_postgres_settings()
    pwd = s.password.get_secret_value()

    driver = (
        "postgresql+asyncpg"
        if s.driver == "asyncpg"
        else "postgresql+psycopg"
    )

    base = f"{driver}://{s.user}:{pwd}@{s.host}:{s.port}/{s.db}"
    params = _build_query_params(s)

    return f"{base}?{params}" if params else base


@lru_cache
def get_async_engine() -> AsyncEngine:
    """
    Async SQLAlchemy 엔진을 생성합니다.

    엔진은 전역 1개를 캐시로 들고 간다.
    종료 시점에 engine.dispose()로 풀 정리를 해야 한다.

    세션을 만들기 위한 기반으로 직접 꺼내 쓰는 경우는 보통 없다.
    """
    s = get_postgres_settings()
    dsn = build_postgres_dsn(s)

    connect_args: dict = {}

    if s.driver == "asyncpg" and s.db_schema:
        connect_args["server_settings"] = {"search_path": s.db_schema}

    return create_async_engine(
        dsn,
        pool_pre_ping=True,
        connect_args=connect_args,
        echo=True,  # 필요 시 SQL 로그
    )


@lru_cache
def get_async_sessionmaker() -> async_sessionmaker[AsyncSession]:
    """
    FastAPI Depends 등에서 재사용할 수 있는 AsyncSession factory.
    """
    engine = get_async_engine()
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
        # autocommit=False, # Default False
    )


async def get_db() -> AsyncGenerator[AsyncSession]:
    AsyncSessionLocal = get_async_sessionmaker()
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise
        finally:
            ...
