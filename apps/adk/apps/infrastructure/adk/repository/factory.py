from __future__ import annotations

from collections.abc import Callable

from google.adk.agents import BaseAgent as ADK_BaseAgent
from google.adk.agents import LlmAgent as ADK_LlmAgent
from google.adk.models import LiteLlm
from google.adk.runners import Runner
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.base_toolset import BaseToolset

from apps.domain.agent import Agent as App_Agent
from apps.infrastructure.session.services.provider import DatabaseSessionServiceEx
from apps.tools import get_weather

type ToolUnion = Callable | BaseTool | BaseToolset
ToolFactory = Callable[[], ToolUnion]
TOOL_REGISTRY: dict[str, ToolFactory] = {
    "get_weather": lambda: get_weather,
    # 필요 시 MCP/OpenAPI toolset도 여기에 팩토리로 등록
}

class AdkFactory:
    def __init__(self, model: LiteLlm):
        self._model = model

    def _build_tool(self,tools: list[str]) -> list[ToolUnion]:
        """ Convert Str -> Callable """
        _tools: list[ToolUnion] = []
        for name in tools:
            factory = TOOL_REGISTRY.get(name)
            if not factory:
                # 정책 선택: (1) 무시 (2) 예외 (3) 로깅 후 무시
                raise ValueError(f"Unknown tool name in DB: {name}")
            _tools.append(factory())
        return _tools

    def _build_agent(
        self,
        agent: App_Agent
    ) -> ADK_BaseAgent:
        """ Convert Agent -> ADK_Agent """
        # TODO: before_model_callback bulder
        match agent.type:
            case 'llm':
                return ADK_LlmAgent(
                    name=agent.name,
                    description=agent.description,
                    # sub_agents: list[BaseAgent] = list,
                    # before_agent_callback: BeforeAgentCallback | None = None,
                    # after_agent_callback: AfterAgentCallback | None = None,
                    model=self._model,
                    instruction=agent.instruction,
                    # global_instruction: str | InstructionProvider = '',
                    # static_instruction: ContentUnion | None = None,
                    tools=self._build_tool(agent.tools),
                    # generate_content_config: GenerateContentConfig | None = None,
                    # disallow_transfer_to_parent: bool = False,
                    # disallow_transfer_to_peers: bool = False,
                    # include_contents: Literal['default', 'none'] = 'default',
                    # input_schema: type[BaseModel] | None = None,
                    # output_schema: type[BaseModel] | None = None,
                    # output_key: str | None = None,
                    # planner: BasePlanner | None = None,
                    # code_executor: BaseCodeExecutor | None = None,
                    # before_model_callback: BeforeModelCallback | None = None,
                    # after_model_callback: AfterModelCallback | None = None,
                    # on_model_error_callback: OnModelErrorCallback | None = None,
                    # before_tool_callback: BeforeToolCallback | None = None,
                    # after_tool_callback: AfterToolCallback | None = None,
                    # on_tool_error_callback: OnToolErrorCallback | None = None
                )
            case _:
                raise ValueError(f"Unknown agent type: {agent.type}")
        # model = LiteLlm(model=.value)  # if USE_OLLAMA else "gemini-2.5-flash"

    def build_runner(
        self,
        agent: App_Agent,
        session: DatabaseSessionServiceEx
    ) -> Runner:
        return Runner(
            # *,
            # app: App | None = None,
            app_name=agent.name, # app_name: str | None = None,
            agent=self._build_agent(agent), # agent: BaseAgent | None = None,
            # plugins: List[BasePlugin] | None = None,
            # artifact_service: BaseArtifactService | None = None,
            session_service=session # session_service: BaseSessionService,
            # memory_service: BaseMemoryService | None = None,
            # credential_service: BaseCredentialService | None = None,
            # plugin_close_timeout: float = 5
        )
