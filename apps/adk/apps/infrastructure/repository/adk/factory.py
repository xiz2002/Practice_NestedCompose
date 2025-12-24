
from typing import Callable, Any
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from apps.infrastructure.repository.sessions.provider import SessionProvider
from google.adk.models.lite_llm import LiteLlm


from google.adk.models.lite_llm import LiteLlm

# os.environ["ADK_APP_NAME"] = "fastapi_adk_demo"
# os.environ["OPENAI_API_KEY"] = "unused"
# os.environ["OLLAMA_KEEP_ALIVE"] = "-1"
# os.environ["OLLAMA_API_BASE"] = "http://ollama:11434"

OLLAMA_MODEL = "qwen3:8b"

class AdkFactory:
    def __init__(self, model: LiteLlm) -> None:
        self._model = model

    def build_agent(self, info: dict[str, Any]) -> Agent:
        model = LiteLlm(model=f"ollama_chat/{OLLAMA_MODEL}") # if USE_OLLAMA else "gemini-2.5-flash"
        return Agent(
            model=model,
            name=info["name"],
            description=info["description"],
            instruction=info["instruction"],
            tools=info["tools"],  
        )

    def build_runner(self, info: dict[str, str | list[Callable[..., Any]]], name: str, session: DatabaseSessionService) -> Runner:
        agent=self.build_agent(info)
        return Runner(agent=agent, 
                      app_name=name, 
                      session_service=session)
