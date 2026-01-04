
# Presentation이 Domain을 import해도 되는가?
# -> 엄격한 의존성 규칙에선 바깥(Presentation)이 안쪽(Domain)을 참조하는 건 허용.
# ※(Domain -> Presentaion은 금지.)
from pydantic import BaseModel, Field

from apps.domain.agent import AgentType


class AgentCreateRequest(BaseModel):
    name: str = Field(..., examples=["agent_name"])
    description: str = Field(..., examples=["agent_description"])
    instruction: str = Field(..., examples=["agent_instruction"])
    tools: list[str] = Field(default_factory=list, examples=[["tool1", "tool2"]])
    type: AgentType = Field(..., examples=["llm"])


class AgentUpdateRequest(BaseModel):
    """
    Agent 갱신시 요청되는 파라메터
    부분 업데이트를 위해 Optinal로 None을 받을 수 있도록 한다.
    """
    name: str | None = None
    description: str | None = None
    instruction: str | None = None
    tools: list[str] | None = None
    type: AgentType | None = None


class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    instruction: str
    tools: list[str]
    type: AgentType
