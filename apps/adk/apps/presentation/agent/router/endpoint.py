from fastapi import APIRouter, Depends

from apps.applications.agent.dto import AgentCreateCommand, AgentUpdateCommand
from apps.applications.agent.usecases import (
    AgentCreateUseCase,
    AgentDeleteUseCase,
    AgentSearchListUseCase,
    AgentSearchUseCase,
    AgentUpdateUseCase,
)
from apps.presentation.agent.mapper import make_create_to_command, make_dto_to_response, make_update_to_command
from apps.presentation.agent.schemas import AgentResponse
from apps.presentation.dependency import (
    get_agent_create_uc,
    get_agent_delete_uc,
    get_agent_get_list_uc,
    get_agent_get_uc,
    get_agent_update_uc,
)

router = APIRouter()


@router.get("", response_model=list[AgentResponse])
async def agents(
    use_case: AgentSearchListUseCase = Depends(get_agent_get_list_uc) # type
):
    """
    Agent 조회
    """
    result = await use_case.execute()
    return [make_dto_to_response(d) for d in result] # type: ignore


@router.get("/{id}", response_model=AgentResponse)
async def agent_info(
    use_case: AgentSearchUseCase = Depends(get_agent_get_uc) # type:
):
    """
    Agent 단일 조회
    """
    result = await use_case.execute()
    return make_dto_to_response(result) # type: ignore


@router.post("", response_model=AgentResponse)
async def create_agent(
    cmd: AgentCreateCommand = Depends(make_create_to_command),
    use_case: AgentCreateUseCase = Depends(get_agent_create_uc) # type: ignore

):
    """
    Agent 생성
    """
    result = await use_case.execute(cmd)
    return make_dto_to_response(result)


@router.delete("/{id}", response_model=AgentResponse)
async def delete_agent(
    use_case: AgentDeleteUseCase = Depends(get_agent_delete_uc)
):
    """
    Agent 삭제
    """
    result = await use_case.execute()
    return make_dto_to_response(result)

@router.patch("/{id}", response_model=AgentResponse)
async def update_agent(
    req: AgentUpdateCommand = Depends(make_update_to_command),
    use_case: AgentUpdateUseCase = Depends(get_agent_update_uc)
):
    """
    Agent 갱신
    """
    result = await use_case.execute(req)
    return make_dto_to_response(result)
