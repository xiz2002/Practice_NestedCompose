from __future__ import annotations

from apps.applications.session.dto import DeleteSessionCommand
from apps.applications.session.ports.adk_gateway import AdkGateway
from apps.domain.session import SessionId, UserId


class DeleteSessionUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway


    async def execute(self, cmd: DeleteSessionCommand) -> bool:
        # 1. Domain 설정
        user_id = UserId(cmd.user_id)
        session_id = SessionId(cmd.session_id)

        # 2. 세션 삭제
        return await self._gateway.session_delete(
            user_id=user_id.value,
            session_id=session_id.value
        )
