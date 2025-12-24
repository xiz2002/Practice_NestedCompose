import os
import litellm

from google.adk.models.lite_llm import LiteLlm

litellm._turn_on_debug() # type: ignore

os.environ["ADK_APP_NAME"] = "fastapi_adk_demo"
os.environ["OPENAI_API_KEY"] = "unused"
os.environ["OLLAMA_KEEP_ALIVE"] = "-1"
os.environ["OLLAMA_API_BASE"] = "http://ollama:11434"

OLLAMA_MODEL = "qwen3:8b"

class LlmModelConfig:
    """ADK에서 사용할 LLM모델을 Ollama로 설정하는 구성 클래스"""
    model: LiteLlm

    def __init__(self) -> None:
        self._model = LiteLlm(model=f"ollama_chat/{OLLAMA_MODEL}") # if USE_OLLAMA else "gemini-2.5-flash"
        
    def __call__(self) -> LiteLlm: 
        return self._model
