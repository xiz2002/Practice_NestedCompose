from __future__ import annotations

from apps.applications.session.dto import GetSessionInfoQuery, SessionInfoResult
from apps.applications.session.ports.adk_gateway import AdkGateway
from apps.domain.session import SessionId, UserId


class ReconnectSessionUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway

    async def execute(self, q: GetSessionInfoQuery) -> SessionInfoResult:
        # 1. Domain 설정
        user_id = UserId(q.user_id)
        session_id = SessionId(q.session_id)

        # 2. 세션 확인
        return await self._gateway.session_exists(
            user_id=user_id.value,
            session_id=session_id.value
        )
