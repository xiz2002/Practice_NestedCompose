from logging.config import fileConfig

from sqlalchemy import pool, MetaData, engine_from_config

from alembic import context
from apps.infrastructure.database.config.postgres import build_postgres_dsn, get_postgres_settings

from google.adk.sessions.database_session_service import Base
from google.adk.sessions.database_session_service import DynamicJSON, PreciseTimestamp, DynamicPickleType

def metadata_with_schema(base_metadata: MetaData, schema: str) -> MetaData:
    md = MetaData(schema=schema)  # 기본 스키마 지정

    for t in base_metadata.sorted_tables:
        # SQLAlchemy 버전에 따라 메서드명이 다를 수 있음
        if hasattr(t, "to_metadata"):
            t.to_metadata(md)      # SA 1.4+ / 2.x
        else:
            t.tometadata(md)       # 구버전 호환

    return md

def render_item(type_, obj, autogen_context):
    """
    커스텀 타입을 마이그레이션 스크립트에서 짧은 이름으로 렌더링하고,
    파일 상단에 필요한 import 문을 자동으로 추가합니다.
    """
    if type_ == 'type':
        # 1. DynamicJSON 처리
        if isinstance(obj, DynamicJSON):
            autogen_context.imports.add("from google.adk.sessions.database_session_service import DynamicJSON")
            return "DynamicJSON()"
        
        # 2. PreciseTimestamp 처리
        if isinstance(obj, PreciseTimestamp):
            autogen_context.imports.add("from google.adk.sessions.database_session_service import PreciseTimestamp")
            return "PreciseTimestamp()"
        
        # 3. DynamicPickleType 처리
        if isinstance(obj, DynamicPickleType):
            autogen_context.imports.add("from google.adk.sessions.database_session_service import DynamicPickleType")
            return "DynamicPickleType()"

    return False

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata_with_schema(Base.metadata, get_postgres_settings().schema)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Postgres 접속 URL 생성
url = build_postgres_dsn(get_postgres_settings())

# 마이그레이션 실행 모드에 따른 처리
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
        version_table_schema=get_postgres_settings().schema
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    section = config.get_section(config.config_ini_section, {})
    section["sqlalchemy.url"] = url.replace("+asyncpg", "").replace("+psycopg", "")
    connectable = engine_from_config(
        # dict(section, **{"sqlalchemy.url": url.replace("+asyncpg", "").replace("+psycopg", "")}),
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            # literal_binds=True,
            include_schemas=True,
            compare_type=True,
            dialect_opts={"paramstyle": "named"},
            render_item=render_item,
            version_table_schema=get_postgres_settings().schema
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
