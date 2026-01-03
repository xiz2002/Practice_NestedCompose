from __future__ import annotations

import uuid

from apps.applications.agent.dto.agent_dto import AgentCreateCommand, AgentDTO
from apps.applications.agent.mapper.mapper import make_dto_from_entity, make_entity_from_create
from apps.applications.agent.ports.agent_repository import AgentRepository


class AgentCreateUseCase:
    def __init__(self, repo: AgentRepository):
        self._repo = repo

    async def execute(self, cmd: AgentCreateCommand) -> AgentDTO:
        agent = make_entity_from_create(str(uuid.uuid4()), cmd)
        saved = await self._repo.save(agent)
        return make_dto_from_entity(saved)
