from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from apps.applications.ports.adk_gateway import AdkGateway
from apps.domain.agent. value_objects import AppName, UserId, SessionId


@dataclass(frozen=True)
class DeleteSessionCommand:
    app_name: str
    user_id: str
    session_id: Optional[str] = None


@dataclass(frozen=True)
class DeleteSessionResult:
    app_name: str
    user_id: str
    session_id: str

class DeleteSessionUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway

    async def execute(self, cmd: DeleteSessionCommand) -> DeleteSessionResult:
        app_name = AppName(cmd.app_name)
        user = UserId(cmd.user_id)
        session = SessionId(cmd.session_id or f"sess_{uuid.uuid4().hex}")

        await self._gateway.session_delete(
            app_name=app_name.value, 
            user_id=user.value, 
            session_id=session.value
        )
        return DeleteSessionResult(app_name=app_name.value, user_id=user.value, session_id=session.value)
