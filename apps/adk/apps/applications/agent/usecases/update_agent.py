from __future__ import annotations

from apps.applications.agent.dto import AgentDTO, AgentUpdateCommand
from apps.applications.agent.mapper import make_dto_from_entity
from apps.applications.agent.services import AgentService


class AgentUpdateUseCase:
    def __init__(self, service: AgentService):
        self._service = service

    async def execute(self, command: AgentUpdateCommand) -> AgentDTO:
        agent = await self._service.get(command.id)

        if agent is None:
            # TODO: Custom Exception
            raise ValueError(f"Agent with id {command.id} not")

        if command.name is not None:
            agent.name = command.name
        if command.description is not None:
            agent.description = command.description
        if command.instruction is not None:
            agent.instruction = command.instruction
        if command.type is not None:
            agent.type = command.type
        if command.tools is not None:
            agent.tools = command.tools

        saved = await self._service.update(agent)

        return make_dto_from_entity(saved)
