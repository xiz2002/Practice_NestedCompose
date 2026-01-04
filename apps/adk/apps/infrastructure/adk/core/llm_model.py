import litellm
from google.adk.models import LiteLlm

# 전역 설정
litellm.use_litellm_proxy = True

class LlmModelConfig:
    """ADK에서 사용할 LLM모델을 설정하는 구성 클래스"""

    def __init__(self, model_id: str, is_debug: bool = False):
        if is_debug:
            litellm._turn_on_debug() # type: ignore

        self._model_id = model_id

    def __call__(self) -> LiteLlm:
        print("LlmModelConfig.__call__")
        return LiteLlm(model=self._model_id)
