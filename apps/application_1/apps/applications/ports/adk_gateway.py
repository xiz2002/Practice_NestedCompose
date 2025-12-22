from __future__ import annotations

from abc import ABC, abstractmethod


class AdkGateway(ABC):
    @abstractmethod
    async def ensure_session(self, user_id: str, session_id: str) -> None:
        """세션이 없으면 생성(있으면 그대로)."""

    @abstractmethod
    async def session_exists(self, user_id: str, session_id: str) -> bool:
        """세션 존재 확인."""

    @abstractmethod
    async def chat(self, user_id: str, session_id: str, message: str) -> str:
        """메시지를 보내고 최종 응답 텍스트 반환."""
