from apps.applications.agent.ports import AgentRepository
from apps.domain.agent import Agent


class AgentService:
    def __init__(self, repo: AgentRepository):
        self._repo = repo

    async def all(self) -> list[Agent]:
        return await self._repo.all()

    async def get(self, id: str) -> Agent:
       return await self._repo.get(id)

    async def save(self, agent: Agent) -> Agent:
        return await self._repo.save(agent)

    async def update(self, agent:Agent) -> Agent:
        return await self.update(agent)

    async def delete(self, id: str) -> Agent:
        return await self._repo.delete(id)
