from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(..., examples=["user123"])
    session_id: str = Field(..., examples=["sess_abc123"])
    message: str = Field(..., examples=["안녕!"])


class ChatResponse(BaseModel):
    session_id: str
    reply: str
