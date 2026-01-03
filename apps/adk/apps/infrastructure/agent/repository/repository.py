from __future__ import annotations

import logging

from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.applications.agent.ports import AgentRepository
from apps.domain.agent.agent import Agent
from apps.infrastructure.agent.mapper import _to_domain
from apps.infrastructure.agent.orm import AgentEntity

# TODO: Logger
logger = logging.getLogger(__name__)

class AgentRepositoryImpl(AgentRepository):
    def __init__(self, session: AsyncSession) -> None:
        """
        Agent Repository

        Attributes:
            session: AsyncSession
        """
        self._session = session

    async def list(self) -> list[Agent]:
        """
        Agent 정보 리스트 취득

        Return:
            list of Agent Domain
        """
        stmt = (
            select(AgentEntity)
            .order_by(AgentEntity.create_time)
        )
        result = await self._session.execute(stmt)
        entities = result.scalars().all()
        return [_to_domain(e) for e in entities]

    async def get(self, id: str) -> Agent:
        """
        Agent 정보 취득

        Args:
            id: AgentEntity Id
        Return:
            None or Agent Domain
        """
        stmt = (
            select(AgentEntity)
            .where(AgentEntity.id == id)
        )
        result = await self._session.scalar(stmt)

        if result is None:
            # TODO: Custom Error
            raise

        return _to_domain(result)

    async def save(self, agent: Agent) -> Agent:
        """
        Agent 정보 저장

        Args:
            id: AgentEntity Id
        Return:
            None or Agent Domain
        """
        stmt = (
            insert(AgentEntity)
            .values(
                id=agent.id,
                name=agent.name,
                description=agent.description,
                instruction=agent.instruction,
                type=agent.type.value,
                tools=agent.tools
            )
            .on_conflict_do_nothing(index_elements=["id"])
            .returning(AgentEntity)
        )
        result = await self._session.execute(stmt)
        entity = result.scalar()
        if entity is None:
            # TODO: Custom Error
            raise
        return _to_domain(entity)

    async def update(self, agent: Agent) -> Agent:
        """
        Agent 정보 갱신

        Args:
            id: AgentEntity Id
        Return:
            None or Agent Domain
        """
        # Build the update statement with all values at once
        update_values = {}
        if agent.name is not None:
            update_values["name"] = agent.name
        if agent.description is not None:
            update_values["description"] = agent.description
        if agent.instruction is not None:
            update_values["instruction"] = agent.instruction
        if agent.type is not None:
            update_values["type"] = agent.type.value
        if agent.tools is not None:
            update_values["tools"] = agent.tools

        if not update_values:
            # If no values to update, return the agent as is
            return agent

        stmt = (
            update(AgentEntity)
            .where(AgentEntity.id == agent.id)
            .values(**update_values)
            .returning(AgentEntity)
        )

        result = await self._session.execute(stmt)
        entity = result.scalar()
        if entity is None:
            # TODO: Custom Error
            raise
        return _to_domain(entity)

    async def delete(self, id: str) -> Agent:
        """
        Agent 정보 삭제

        Args:
            id: AgentEntity Id
        """
        stmt = (
            delete(AgentEntity)
            .where(AgentEntity.id == id)
            .returning(AgentEntity)
        )


        result = await self._session.execute(stmt)
        entity = result.scalar()
        if entity is None:
            # TODO: Custom Error
            raise

        # logger.debug(entity)
        return _to_domain(entity)


