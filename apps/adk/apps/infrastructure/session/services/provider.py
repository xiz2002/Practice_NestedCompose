from __future__ import annotations

import asyncio
import logging
from typing import override

from google.adk.sessions.database_session_service import DatabaseSessionService
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
)
from sqlalchemy.schema import MetaData
from tzlocal import get_localzone


class DatabaseSessionServiceEx(DatabaseSessionService):
    @override
    def __init__(self, engine: AsyncEngine, maker: async_sessionmaker):
        """Initializes the database session service with a database URL."""
        # # Get the local timezone
        # local_timezone = get_localzone()
        # logger = logging.getLogger("google_adk." + __name__)
        # logger.info("Local timezone: %s", local_timezone)

        # self.db_engine: AsyncEngine = engine
        # self.metadata: MetaData = MetaData()

        # # DB session factory method
        # self.database_session_factory: async_sessionmaker[AsyncSession] = \
        # async_sessionmaker(bind=self.db_engine, expire_on_commit=False)

        # # Flag to indicate if tables are created
        # self._tables_created = False
        # # Lock to ensure thread-safe table creation
        # self._table_creation_lock = asyncio.Lock()

        # Get the local timezone
        local_timezone = get_localzone()
        logger = logging.getLogger("google_adk." + __name__)
        logger.info("Local timezone: %s", local_timezone)

        self.db_engine: AsyncEngine = engine
        self.metadata: MetaData = MetaData()

        # DB session factory method
        self.database_session_factory = maker

        # Flag to indicate if tables are created
        self._tables_created = True

        # Lock to ensure thread-safe table creation
        self._table_creation_lock = asyncio.Lock()


class SessionProvider:
    """ """
    def __init__(self, engine: AsyncEngine, maker: async_sessionmaker):
        self._engine = engine
        self._maker = maker

    def __call__(self) -> DatabaseSessionServiceEx:
        print("SessionProvicer.__call__")
        return DatabaseSessionServiceEx(engine=self._engine, maker=self._maker)

    # def build_session_service() -> DatabaseSessionService:
    # return DatabaseSessionService(
            # build_postgres_dsn(),
            # connect_args={"server_settings": {"search_path": self._config.schema}}
    # )
