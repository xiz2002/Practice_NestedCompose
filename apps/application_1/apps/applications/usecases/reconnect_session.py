from __future__ import annotations

from dataclasses import dataclass

from apps.applications.ports.adk_gateway import AdkGateway
from apps.domain.agent.value_objects import UserId, SessionId


@dataclass(frozen=True)
class ReconnectSessionQuery:
    user_id: str
    session_id: str


@dataclass(frozen=True)
class ReconnectSessionResult:
    exists: bool
    user_id: str
    session_id: str


class ReconnectSessionUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway

    async def execute(self, q: ReconnectSessionQuery) -> ReconnectSessionResult:
        user = UserId(q.user_id)
        session = SessionId(q.session_id)

        exists = await self._gateway.session_exists(user_id=user.value, session_id=session.value)
        return ReconnectSessionResult(exists=exists, user_id=user.value, session_id=session.value)
