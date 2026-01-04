
from apps.domain.agent import Agent, AgentType
from apps.infrastructure.agent.orm.agents import AgentEntity


def _to_domain(e: AgentEntity) -> Agent:
    """
    Mapper: Infastructure -> Domain
    Converts a AgentEntiry to Domain Model.

    Examples:
    ```
    _to_domain(e) -> Agent(...)
    [_to_domain(e) for e in entities] -> [Agent(...), ...]]
    ```

    Args:
        e: AgentEntity

    Returns:
        Agent Domain Model
    """

    try:
        agent_type = AgentType(e.type)
    except ValueError:
        raise ValueError(f"Invalid AgentType from DB: {e.type}")

    return Agent(
        id=str(e.id),
        name=e.name,
        description=e.description,
        instruction=e.instruction,
        type=agent_type,
        tools=list(e.tools) if e.tools else [],
    )
