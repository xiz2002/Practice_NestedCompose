from fastapi import APIRouter

from .agent.router.endpoint import router as agent_router
from .chat.router.endpoint import router as chat_router
from .health.router.endpoint import router as health_router
from .session.router.endpoint import router as sessions_router

router = APIRouter()
router.include_router(agent_router, prefix="/agent", tags=["Agent"])
router.include_router(sessions_router, prefix="/{agent_id}/session", tags=["Sessions"])
router.include_router(chat_router, prefix="/{agent_id}/{session_id}/chat", tags=["Chat"])
router.include_router(health_router, prefix="/health", tags=["Health"])
