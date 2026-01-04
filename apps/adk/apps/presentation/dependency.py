
from fastapi import Depends
from google.adk.models.lite_llm import LiteLlm
from sqlalchemy.ext.asyncio import AsyncSession

from apps.applications.agent.ports import AgentRepository
from apps.applications.agent.services import AgentService
from apps.applications.agent.usecases import (
    AgentCreateUseCase,
    AgentDeleteUseCase,
    AgentSearchListUseCase,
    AgentSearchUseCase,
    AgentUpdateUseCase,
)
from apps.applications.session.usecases.chat import ChatUseCase
from apps.applications.session.usecases.create_session import CreateSessionUseCase
from apps.applications.session.usecases.delete_session import DeleteSessionUseCase
from apps.applications.session.usecases.reconnect_session import ReconnectSessionUseCase
from apps.infrastructure._database.config.postgres import get_async_engine, get_async_sessionmaker, get_db
from apps.infrastructure.adk.core.llm_model import LlmModelConfig
from apps.infrastructure.adk.repository.factory import AdkFactory
from apps.infrastructure.adk.repository.gateway import AdkGatewayImpl
from apps.infrastructure.agent.repository.repository import AgentRepositoryImpl
from apps.infrastructure.session.services.provider import DatabaseSessionServiceEx, SessionProvider

# from apps.tools.weather import get_weather

# only_seoul_weather = partial(get_weather, city_name="Seoul")

# agent_info: dict[str, str | list[Callable[..., Any]]] = {
#     "name": "demo_agent",
#     "description": "Ollama를 사용하는 로컬 에이전트입니다.",
#     "instruction": """
# 도시 이름을 입력하면 해당 도시의 날씨 정보를 제공한다.
# - 사용자가 '날씨'를 확인하는 의도일 때만 tool `get_weather`를 호출한다.
# - tool 호출 결과에는 반드시 검색한 필드를 같이 출력한다.:
#   1) city_name (질의문)
# - target을 특정할 수 없으면 tool을 호출하지 말고, target을 고르는 질문 1개만 한다.
# """,
#     "tools": [get_weather],
# }

# ---------------------------------------------
#
# ---------------------------------------------
def get_agent_repository(
    session: AsyncSession = Depends(get_db)
) -> AgentRepository:
    return AgentRepositoryImpl(session=session)

def provide_agent_service(
    repo: AgentRepository = Depends(get_agent_repository)
) -> AgentService:
    return AgentService(repo=repo)

def get_agent_get_uc(
    id: str,
    service: AgentService = Depends(provide_agent_service)
) -> AgentSearchUseCase:
    return AgentSearchUseCase(id=id, service=service)

def get_agent_get_list_uc(
    service: AgentService = Depends(provide_agent_service)
) -> AgentSearchListUseCase:
    return AgentSearchListUseCase(service=service)

def get_agent_create_uc(
    service: AgentService = Depends(provide_agent_service)
) -> AgentCreateUseCase:
    return AgentCreateUseCase(service=service)

def get_agent_update_uc(
    service: AgentService = Depends(provide_agent_service)
) -> AgentUpdateUseCase:
    return AgentUpdateUseCase(service=service)

def get_agent_delete_uc(
    id: str,
    service: AgentService = Depends(provide_agent_service)
) -> AgentDeleteUseCase:
    return AgentDeleteUseCase(id=id, service=service)

# ---------------------------------------------
#
# ---------------------------------------------
def get_agent_id_from_path_param(agent_id: str) -> str:
    return agent_id

# Make LlmModelConfig injectable
def get_llm_model_config():
    return LlmModelConfig(
        model_id="ollama-qwen3-4b",
        is_debug=True
    )

def get_session_service():
    return SessionProvider(
        engine=get_async_engine(),
        maker=get_async_sessionmaker()
    )

async def get_gateway(
    agent_id: str = Depends(get_agent_id_from_path_param),
    agent_repo: AgentRepository = Depends(get_agent_repository),
    session: DatabaseSessionServiceEx = Depends(get_session_service()),
    litellm: LiteLlm = Depends(get_llm_model_config()),
) -> AdkGatewayImpl:
    return AdkGatewayImpl(
        agent_info=await agent_repo.get(agent_id),
        service=session,
        factory=AdkFactory(litellm)
    )

def get_create_session_uc(
    gateway: AdkGatewayImpl = Depends(get_gateway)
) -> CreateSessionUseCase:
    return CreateSessionUseCase(gateway=gateway)


def get_reconnect_session_uc(
    gateway: AdkGatewayImpl = Depends(get_gateway)
) -> ReconnectSessionUseCase:
    return ReconnectSessionUseCase(gateway=gateway)


def get_delete_session_uc(
    gateway: AdkGatewayImpl = Depends(get_gateway)
) -> DeleteSessionUseCase:
    return DeleteSessionUseCase(gateway=gateway)


def get_chat_uc(
    gateway: AdkGatewayImpl = Depends(get_gateway)
) -> ChatUseCase:
    return ChatUseCase(gateway=gateway)

def get_chat_uc_sse(
    gateway: AdkGatewayImpl = Depends(get_gateway)
) -> ChatUseCase:
    return ChatUseCase(gateway=gateway)

