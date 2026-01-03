from __future__ import annotations

from dataclasses import dataclass

from apps.applications.session.ports.adk_gateway import AdkGateway
from apps.domain.agent.value_objects import SessionId, UserId


@dataclass(frozen=True)
class ChatCommand:
    user_id: str
    session_id: str
    message: str


@dataclass(frozen=True)
class ChatResult:
    session_id: str
    reply: str


class ChatUseCase:
    def __init__(self, gateway: AdkGateway) -> None:
        self._gateway = gateway

    async def execute(self, cmd: ChatCommand) -> ChatResult:
        user = UserId(cmd.user_id)
        session = SessionId(cmd.session_id)

        # 세션은 존재해야 한다는 정책(없으면 404는 Presentation에서 처리)
        reply = await self._gateway.chat(
            user_id=user.value,
            session_id=session.value,
            message=cmd.message,
        )
        return ChatResult(session_id=session.value, reply=reply)
