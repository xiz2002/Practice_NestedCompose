# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:/root/.local/bin:${PATH}"

# 런타임에 필요한 시스템 라이브러리만 (psycopg2 등에서 필요)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# uv 설치 (프로덕션에서도 재현성 있게 설치하기 위함)
#RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# 의존성 파일만 먼저 복사해서 레이어 캐시 효율화
# (프로젝트가 uv를 사용한다는 전제: pyproject.toml + uv.lock)
COPY pyproject.toml uv.lock ./

# 의존성 설치 (lock 기준, venv 생성)
RUN uv sync --frozen --no-dev

# 애플리케이션 소스 복사
COPY apps ./apps

# 비루트 사용자로 실행 (기본쉘을 bash로 변경)
RUN useradd -m -u 10001 -s /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 선택: 헬스체크 (엔드포인트는 실제 프로젝트에 맞게 수정)
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -fsS http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "apps.presentation.api:app", "--host", "0.0.0.0", "--port", "8000"]
