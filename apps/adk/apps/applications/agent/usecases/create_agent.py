from __future__ import annotations

import uuid

from apps.applications.agent.dto import AgentCreateCommand, AgentDTO
from apps.applications.agent.mapper import make_dto_from_entity, make_entity_from_create
from apps.applications.agent.services import AgentService


class AgentCreateUseCase:
    def __init__(self, service: AgentService):
        self._service = service

    async def execute(self, cmd: AgentCreateCommand) -> AgentDTO:
        agent = make_entity_from_create(str(uuid.uuid4()), cmd)
        saved = await self._service.save(agent)
        return make_dto_from_entity(saved)
