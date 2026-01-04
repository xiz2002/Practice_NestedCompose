from dataclasses import dataclass

from .types import AgentType


@dataclass()
class Agent:
    id: str
    name: str
    description: str
    instruction: str
    type: AgentType
    tools: list[str]

