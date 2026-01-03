from __future__ import annotations

from apps.applications.agent.dto.agent_dto import AgentDTO
from apps.applications.agent.mapper.mapper import make_dto_from_entity
from apps.applications.agent.ports.agent_repository import AgentRepository


class AgentSearchUseCase:
    def __init__(self, agent_id: str, repo: AgentRepository):
        self._agent_id = agent_id
        self._repo = repo

    async def execute(self) -> AgentDTO:
        agent = await self._repo.get(self._agent_id)
        return make_dto_from_entity(agent)
