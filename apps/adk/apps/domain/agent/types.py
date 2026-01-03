from enum import Enum


# AgentType = Literal["llm", "sequential", "parallel", "loop"]
class AgentType(str, Enum):
    LLM = "llm"
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    LOOP = "loop"
