from __future__ import annotations

from apps.applications.agent.dto import AgentDTO
from apps.applications.agent.mapper import make_dto_from_entity
from apps.applications.agent.services import AgentService


class AgentSearchListUseCase:
    def __init__(self, service: AgentService):
        self._service = service

    async def execute(self) -> list[AgentDTO]:
        agents = await self._service.all()
        return [make_dto_from_entity(e) for e in agents]
