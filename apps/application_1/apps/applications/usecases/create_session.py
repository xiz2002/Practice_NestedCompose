from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from apps.applications.ports.adk_gateway import AdkGateway
from apps.domain.agent. value_objects import UserId, SessionId


@dataclass(frozen=True)
class CreateSessionCommand:
    user_id: str
    session_id: Optional[str] = None


@dataclass(frozen=True)
class CreateSessionResult:
    user_id: str
    session_id: str


class CreateSessionUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway

    async def execute(self, cmd: CreateSessionCommand) -> CreateSessionResult:
        user = UserId(cmd.user_id)
        session = SessionId(cmd.session_id or f"sess_{uuid.uuid4().hex}")

        await self._gateway.ensure_session(user_id=user.value, session_id=session.value)
        return CreateSessionResult(user_id=user.value, session_id=session.value)
