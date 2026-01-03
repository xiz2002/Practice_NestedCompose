from __future__ import annotations

from apps.applications.agent.dto.agent_dto import AgentDTO
from apps.applications.agent.mapper.mapper import make_dto_from_entity
from apps.applications.agent.ports.agent_repository import AgentRepository


class AgentSearchListUseCase:
    def __init__(self, repo: AgentRepository):
        self._repo = repo

    async def execute(self) -> list[AgentDTO]:
        agents = await self._repo.list()
        return [make_dto_from_entity(e) for e in agents]
