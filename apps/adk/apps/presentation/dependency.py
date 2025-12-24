from typing import Callable, Any
from fastapi import Depends
from functools import lru_cache, partial

from apps.applications.usecases.chat import ChatUseCase
from apps.applications.usecases.create_session import CreateSessionUseCase
from apps.applications.usecases.delete_session import DeleteSessionUseCase
from apps.applications.usecases.reconnect_session import ReconnectSessionUseCase

from apps.infrastructure.repository.adk.core.llm_model import LlmModelConfig
from apps.infrastructure.repository.adk.factory import AdkFactory
from apps.infrastructure.repository.adk.gateway import AdkGatewayImpl

from apps.infrastructure.repository.sessions.provider import SessionProvider

from apps.tools.weather import get_weather

from apps.infrastructure.database.config.postgres import PostgresSettings, get_postgres_settings

APPLICATION_NAME = "Application_Name"

only_seoul_weather = partial(get_weather, city_name="Seoul")

agent_info: dict[str, str | list[Callable[..., Any]]] = {
    "name": "demo_agent",
    "description": "Ollama를 사용하는 로컬 에이전트입니다.",
    "instruction": 
"""
도시 이름을 입력하면 해당 도시의 날씨 정보를 제공한다.
- 사용자가 '날씨'를 확인하는 의도일 때만 tool `get_weather`를 호출한다.
- tool 호출 결과에는 반드시 검색한 필드를 같이 출력한다.:
  1) city_name (질의문)
- target을 특정할 수 없으면 tool을 호출하지 말고, target을 고르는 질문 1개만 한다.
""",
    "tools": [get_weather],
}

service = PostgresSettings

@lru_cache(maxsize=1)
def get_gateway() -> AdkGatewayImpl:
    runner=AdkFactory(LlmModelConfig()()).build_runner(agent_info, APPLICATION_NAME, SessionProvider(get_postgres_settings())())
    return AdkGatewayImpl(runner)


def get_app_name() -> str:
    return APPLICATION_NAME


def get_create_session_uc() -> CreateSessionUseCase:
    return CreateSessionUseCase(gateway=get_gateway())


def get_reconnect_session_uc() -> ReconnectSessionUseCase:
    return ReconnectSessionUseCase(gateway=get_gateway())


def get_chat_uc() -> ChatUseCase:
    return ChatUseCase(gateway=get_gateway())


def get_delete_session_uc() -> DeleteSessionUseCase:
    return DeleteSessionUseCase(gateway=get_gateway())