from collections.abc import Callable
from typing import Any

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService


class AdkFactory:
    def __init__(self, model: LiteLlm) -> None:
        self._model = model

    def build_agent(self, info: dict[str, Any]) -> Agent:
        # model = LiteLlm(model=.value)  # if USE_OLLAMA else "gemini-2.5-flash"
        return Agent(
            model=self._model,
            name=info["name"],
            description=info["description"],
            instruction=info["instruction"],
            tools=info["tools"],
        )

    def build_runner(
        self, info: dict[str, str | list[Callable[..., Any]]], name: str, session: DatabaseSessionService
    ) -> Runner:
        agent = self.build_agent(info)
        return Runner(agent=agent, app_name=name, session_service=session)
