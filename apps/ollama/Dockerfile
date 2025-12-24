FROM ollama/ollama:latest AS ROOT

COPY ./models ./models

RUN ollama serve \
    & sleep 5 \
    # && ollama create Qwan3-VL-8B-Custom:Q4_K_M -f ./models/Qwen3VL-8B-Instruct-Q4_K_M/Modelfile \
    && ollama create qwen3-Q4_K_M:4b -f ./models/Qwen3-4B-Q4_K_M/Modelfile

 ENTRYPOINT ["ollama", "serve"]