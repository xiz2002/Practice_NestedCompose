from __future__ import annotations

from apps.applications.agent.dto.agent_dto import AgentDTO
from apps.applications.agent.mapper.mapper import make_dto_from_entity
from apps.applications.agent.ports.agent_repository import AgentRepository


class AgentDeleteUseCase:
    def __init__(self, id: str, repo: AgentRepository):
        self._id = id
        self._repo = repo

    async def execute(self) -> AgentDTO:
        result = await self._repo.delete(self._id)

        return make_dto_from_entity(result)
