from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    user_id: str = Field(..., examples=["user123"])
    message: str = Field(..., examples=["안녕!"])
    is_sse: bool = False


class ChatResponse(BaseModel):
    reply: str
