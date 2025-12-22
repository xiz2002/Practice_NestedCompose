import os
import litellm
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.models.lite_llm import LiteLlm

from apps.infrastructure.database.config.postgres import get_postgres_settings, build_postgres_dsn, build_postgres_dsn_sync

litellm._turn_on_debug() # type: ignore

service = get_postgres_settings()
APP_NAME = "ABCD"
DB_URL = build_postgres_dsn(service)

os.environ["ADK_APP_NAME"] = "fastapi_adk_demo"

os.environ["OLLAMA_KEEP_ALIVE"] = "-1"
#
os.environ["OLLAMA_API_BASE"] = "http://ollama:11434"
#
os.environ["OPENAI_API_KEY"] = "unused"

OLLAMA_MODEL = "qwen3:8b"
MODEL_ID = LiteLlm(model=f"ollama_chat/{OLLAMA_MODEL}") # if USE_OLLAMA else "gemini-2.5-flash"

def build_agent() -> Agent:
    return Agent(
        name="demo_agent",
        model=MODEL_ID,
        description="Ollama를 사용하는 로컬 에이전트입니다.",
        instruction="당신은 로컬에서 실행되는 유능한 비서입니다.",
    )


def build_session_service() -> DatabaseSessionService:
    return DatabaseSessionService(
        build_postgres_dsn_sync(),
        # execution_options={"schema_translate_map": {None, service.schema}}
        connect_args={"options": f"-c search_path={service.schema}"},
    )


def build_runner() -> Runner:
    agent = build_agent()
    session_service = build_session_service()
    return Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
