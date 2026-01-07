from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from apps.applications.session.dto import SessionInfoResult


class AdkGateway(ABC):
    @abstractmethod
    async def ensure_session(self, user_id: str, session_id: str, state: dict[str, Any] | None) -> SessionInfoResult:
        """세션이 없으면 생성(있으면 그대로)."""

    @abstractmethod
    async def session_delete(self, user_id: str, session_id: str) -> bool:
        """존재하는 세션을 삭제."""

    @abstractmethod
    async def session_exists(self, user_id: str, session_id: str) -> SessionInfoResult:
        """세션 존재 확인."""

    @abstractmethod
    async def chat_events(self, user_id: str, session_id: str, message: str) -> str:
        """메시지를 보내고 최종 응답 텍스트 반환."""

    @abstractmethod
    def chat_events_sse(self, user_id: str, session_id: str, message: str) -> AsyncIterator[dict[str, Any]]:
        """메시지를 보내고 스트림 반환."""
