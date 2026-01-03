"""
① Presentation → Application (Request → Command)

AgentCreateRequest → CreateAgentCommand

AgentUpdateRequest + id → UpdateAgentCommand

✔ HTTP/API 관심사 제거
✔ validation 종료 지점
"""


# from applications.agent.dto.agent_dto import AgentDTO
from apps.applications.agent.dto.agent_dto import AgentCreateCommand, AgentDTO, AgentUpdateCommand
from apps.presentation.agent.schemas.agent import AgentCreateRequest, AgentResponse, AgentUpdateRequest


# ------------------------------------------
# Presentation -> Application
# ------------------------------------------
def make_create_to_command(req: AgentCreateRequest) -> AgentCreateCommand:
    return AgentCreateCommand(
        name=req.name,
        description=req.description,
        instruction=req.instruction,
        type=req.type,
        tools=list(req.tools),
    )

def make_update_to_command(id: str, req: AgentUpdateRequest) -> AgentUpdateCommand:
    return AgentUpdateCommand(
        id=id,
        name=req.name if req.name is not None else None,
        description=req.description if req.description is not None else None,
        instruction=req.instruction if req.instruction is not None else None,
        type=req.type if req.type is not None else None,
        tools=req.tools if req.tools is not None else None
    )


# ------------------------------------------
# Application -> Presentation
# ------------------------------------------
def make_dto_to_response(agent: AgentDTO) -> AgentResponse:
    return AgentResponse(
        id=agent.id,
        name=agent.name,
        description=agent.description,
        instruction=agent.instruction,
        type=agent.type,
        tools=agent.tools
    )
