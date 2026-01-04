
from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    user_id: str = Field(..., examples=["user123"])

class DeleteSessionRequest(BaseModel):
    user_id: str = Field(..., examples=["user123"])
    session_id: str = Field(..., examples=["sess_abc123"])

class SessionInfoResponse(BaseModel):
    app_name: str
    user_id: str
    session_id: str
    state: dict
    exists: bool
