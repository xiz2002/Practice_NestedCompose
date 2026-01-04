from __future__ import annotations

from typing import Protocol

from apps.domain.agent import Agent


class AgentRepository(Protocol):
    async def all(self) -> list[Agent]: ...
    """Agent 리스트 취득"""

    async def get(self, id: str) -> Agent: ...
    """Agent 취득"""

    async def save(self, agent: Agent) -> Agent: ...
    """Agent 생성"""

    async def update(self, agent: Agent) -> Agent: ...
    """Agent 생성"""

    async def delete(self, id: str) -> Agent: ...
    """Agent 삭제."""
