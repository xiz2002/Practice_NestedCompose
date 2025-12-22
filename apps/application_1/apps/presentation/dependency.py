from functools import lru_cache

from apps.applications.usecases.chat import ChatUseCase
from apps.applications.usecases.create_session import CreateSessionUseCase
from apps.applications.usecases.reconnect_session import ReconnectSessionUseCase
from apps.infrastructure.repository.adk.factory import build_runner, APP_NAME
from apps.infrastructure.repository.adk.gateway import AdkGatewayImpl

from apps.infrastructure.database.config.postgres import get_postgres_settings


@lru_cache(maxsize=1)
def get_gateway() -> AdkGatewayImpl:
    # runner는 무겁고 전역으로 공유하는 게 일반적
    runner = build_runner()
    return AdkGatewayImpl(runner=runner)


def get_app_name() -> str:
    return APP_NAME


def get_create_session_uc() -> CreateSessionUseCase:
    return CreateSessionUseCase(gateway=get_gateway())


def get_reconnect_session_uc() -> ReconnectSessionUseCase:
    return ReconnectSessionUseCase(gateway=get_gateway())


def get_chat_uc() -> ChatUseCase:
    return ChatUseCase(gateway=get_gateway())
