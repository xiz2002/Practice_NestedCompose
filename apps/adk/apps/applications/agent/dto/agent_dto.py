from dataclasses import dataclass, field

from apps.domain.agent.types import AgentType


@dataclass
class AgentCreateCommand:
    name: str
    description: str
    instruction: str
    type: AgentType
    tools: list[str] = field(default_factory=list)

@dataclass
class AgentUpdateCommand:
    id: str
    name: str | None = None
    description: str | None = None
    instruction: str | None = None
    type: AgentType | None = None
    tools: list[str] | None = None

@dataclass
class AgentDTO:
    id: str
    name: str
    description: str
    instruction: str
    type: AgentType
    tools: list[str] = field(default_factory=list)
