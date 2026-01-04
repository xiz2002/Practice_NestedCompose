from __future__ import annotations

from apps.applications.agent.dto.dto_agent import AgentDTO
from apps.applications.agent.mapper import make_dto_from_entity
from apps.applications.agent.services import AgentService


class AgentDeleteUseCase:
    def __init__(self, id: str, service: AgentService):
        self._id = id
        self._service = service

    async def execute(self) -> AgentDTO:
        result = await self._service.delete(self._id)

        return make_dto_from_entity(result)
