import logging
import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .routers import router as root_router

_PREFIX = os.getenv("PREFIX", "/api/v1")

class HealthCheckFilter(logging.Filter):
    def filter(self, record):
        return "/api/v1/health" not in record.getMessage()

def apply_access_log_filter() -> None:
    """uvicorn.access 로그/핸들러에 health 필터를 적용한다."""
    access_logger = logging.getLogger("uvicorn.access")
    flt = HealthCheckFilter()

    # 로거 자체에도 추가
    access_logger.addFilter(flt)

    # 이미 달려있는 핸들러에도 추가
    for h in access_logger.handlers:
        h.addFilter(flt)

# Application
app = FastAPI(
    title="Web Application",
    description="",
    version="0.1.0",
    servers=[{"url":"http://localhost:8000","description":""}]
)

# 3) 로깅 필터 적용 (app import 시점에 실행)
apply_access_log_filter()

# 루트 페이지 (Docs 출력)
@app.get("", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# 메인 라우터
app.include_router(root_router, prefix=_PREFIX)
