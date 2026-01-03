from __future__ import annotations

from apps.applications.agent.dto.agent_dto import AgentDTO, AgentUpdateCommand
from apps.applications.agent.mapper.mapper import make_dto_from_entity
from apps.applications.agent.ports.agent_repository import AgentRepository


class AgentUpdateUseCase:
    def __init__(self, repo: AgentRepository):
        self._repo = repo

    async def execute(self, command: AgentUpdateCommand) -> AgentDTO:
        agent = await self._repo.get(command.id)

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

        saved = await self._repo.update(agent)

        return make_dto_from_entity(saved)
