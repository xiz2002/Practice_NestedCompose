from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

from apps.applications.session.ports.adk_gateway import AdkGateway
from apps.domain.session.value_object_session import SessionId, UserId


@dataclass(frozen=True)
class ChatCommand:
    user_id: str
    session_id: str
    message: str
    is_sse: bool


@dataclass(frozen=True)
class ChatResult:
    reply: str


class ChatUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway

    async def execute(self, cmd: ChatCommand) -> ChatResult:
        user = UserId(cmd.user_id)
        session = SessionId(cmd.session_id)

        # 세션은 존재해야 한다는 정책(없으면 404는 Presentation에서 처리)
        reply = await self._gateway.chat_events(
            user_id=user.value,
            session_id=session.value,
            message=cmd.message
        )
        return ChatResult(reply=reply)

    def execute_sse(self, cmd: ChatCommand) -> AsyncIterator[dict[str, Any]]:
        user = UserId(cmd.user_id)
        session = SessionId(cmd.session_id)

        # 세션은 존재해야 한다는 정책(없으면 404는 Presentation에서 처리)
        return self._gateway.chat_events_sse(
            user_id=user.value,
            session_id=session.value,
            message=cmd.message,
        )

