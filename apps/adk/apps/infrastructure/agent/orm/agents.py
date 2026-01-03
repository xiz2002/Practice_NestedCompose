from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import DateTime, String

DEFAULT_MAX_KEY_LENGTH = 128
DEFAULT_MAX_VARCHAR_LENGTH = 256

class Base(DeclarativeBase):
    pass

class AgentEntity(Base):
    """agent stored in the database."""

    __tablename__ = "agents"
    __table_args__ = {"schema": "adk"}
    id: Mapped[str] = mapped_column(String(DEFAULT_MAX_KEY_LENGTH), primary_key=True)
    name: Mapped[str] = mapped_column(String(DEFAULT_MAX_VARCHAR_LENGTH))
    description: Mapped[str] = mapped_column(String(DEFAULT_MAX_VARCHAR_LENGTH))
    instruction: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(DEFAULT_MAX_VARCHAR_LENGTH))
    tools: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=False, server_default="{}")
    create_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    update_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
