from typing import Optional
from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    user_id: str = Field(..., examples=["user123"])
    session_id: Optional[str] = Field(None, examples=["sess_abc123"])


class CreateSessionResponse(BaseModel):
    app_name: str
    user_id: str
    session_id: str


class SessionInfoResponse(BaseModel):
    exists: bool
    app_name: str
    user_id: str
    session_id: str
