## Example
# echo FROM path/to/my/model.gguf > Modelfile
# echo SYSTEM '"""You are an assistant that discusses with customers in a friendly way"""' >> Modelfile
# ollama show --modelfile qwen3:4b | grep -v "^FROM" >> Modelfile
# ollama create my-new-model

# ollama show <Model> --modelfile
# ollama show <Model>
# FROM에는 GGUF 형식 모델 등 추가하고자 하는 모델의 경로와 이름을 넣습니다.
FROM hf.co/Qwen/Qwen3-VL-8B-Instruct-GGUF:Q4_K_M

# PARAMETER에서는 모델의 세부 설정을 할 수 있습니다.
## 모델이 얼마나 창의적으로 답변할 것인지 결정하는 부분입니다. 
## 0~1까지 설정 할 수 있으며 높을 수록 창의적인 답변을 내놓습니다. 기본 값은 0.8입니다.
PARAMETER temperature 1

## 그 전의 답변을 얼마나 기억해 다음 답변에 반영할 것인지 결정하는 부분입니다.
## 값을 높게 줄수록 하드웨어 및 성능에 영향을 줍니다. 기본 값은 2048입니다.
PARAMETER num_ctx 4096

## 모델이 답변에 사용할 수 있는 토큰의 수를 의미합니다. 기본값은 128입니다.
PARAMETER num_predict 128

# 시스템의 역할을 부여해 모델의 답변을 어느정도 유도할 수 있습니다.
SYSTEM """You are an assistant designed for question-answering tasks. Use the provided pieces of retrieved context to answer the questions accurately. Ensure that your answers are directly relevant to the questions and cite your sources when possible. Keep your respoinses concise and within three setences. 당신은 질문에 답변하는 데 특화된 도우미입니다. 제공된 정보를 화라용하여 질문에 정확하게 답변하십시오. 답변은 질문과 직접적인 관련이 있어야 하며, 가능한 경우 출저를 명시하십시오. 답변은 간결하게 세 문장 이내로 작성하십시오."""

### SAMPLE ###
# FROM hf.co/Qwen/Qwen3-VL-8B-Instruct-GGUF:Q4_K_M
FROM Qwan3-VL-8B-Custom:Q4_K_M

TEMPLATE "{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>

SYSTEM """You are an assistant designed for question-answering tasks. Use the provided pieces of retrieved context to answer the questions accurately. Ensure that your answers are directly relevant to the questions and cite your sources when possible. 당신은 질문에 답변하는 데 특화된 도우미입니다. 제공된 정보를 활용하여 질문에 정확하게 답변하십시오. 답변은 질문과 직접적인 관련이 있어야 하며, 가능한 경우 출저를 명시하십시오."""

PARAMETER stop <|im_start|>
PARAMETER stop <|im_end|>
PARAMETER stop <|im_start|>user