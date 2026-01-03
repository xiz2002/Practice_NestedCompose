from apps.applications.agent.dto.agent_dto import AgentCreateCommand, AgentDTO
from apps.domain.agent.agent import Agent

"""
② Application → Domain (Command → Entity)

CreateAgentCommand → Agent

UpdateAgentCommand + Agent → Agent

✔ 비즈니스 모델 생성/갱신
✔ 도메인 불변성 유지

📍 이건 Application 레이어 책임
→ applications/agent/mappers
"""

# ------------------------------------------
# Application -> Domain
# ------------------------------------------
def make_entity_from_create(id: str, cmd: AgentCreateCommand) -> Agent:
    return Agent(
        id=id,
        name=cmd.name,
        description=cmd.description,
        instruction=cmd.instruction,
        type=cmd.type,
        tools=cmd.tools
    )

# ------------------------------------------
# Domain -> Application
# ------------------------------------------
def make_dto_from_entity(agent: Agent) -> AgentDTO:
    return AgentDTO(
        id=agent.id,
        name=agent.name,
        description=agent.description,
        instruction=agent.instruction,
        tools=list(agent.tools),
        type=agent.type,
    )
