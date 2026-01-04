from __future__ import annotations

import uuid

from apps.applications.session.dto import CreateSessionCommand, SessionInfoResult
from apps.applications.session.ports.adk_gateway import AdkGateway
from apps.domain.session import SessionId, UserId


class CreateSessionUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway

    async def execute(self, cmd: CreateSessionCommand) -> SessionInfoResult:
        # 1. Domain 설정
        user_id = UserId(cmd.user_id)
        session_id = SessionId(str(uuid.uuid4()))

        # 2. 세션 등록
        return await self._gateway.ensure_session(
            user_id=user_id.value,
            session_id=session_id.value
        )
