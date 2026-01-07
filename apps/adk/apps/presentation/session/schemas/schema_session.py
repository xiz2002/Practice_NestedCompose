
from typing import Any

from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    user_id: str = Field(..., examples=["user123"])
    state: dict[str, Any] | None = None

class DeleteSessionRequest(BaseModel):
    user_id: str = Field(..., examples=["user123"])
    session_id: str = Field(..., examples=["537b078f-c809-40b8-aabf-558347c0df81"])

class SessionInfoResponse(BaseModel):
    app_name: str
    user_id: str
    session_id: str
    state: dict
    exists: bool
