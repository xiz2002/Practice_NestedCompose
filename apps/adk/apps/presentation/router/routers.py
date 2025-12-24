from fastapi import APIRouter
from .health.endpoint import router as health_router
from .agent.endpoint import router as agent_router
from .sessions.endpoint import router as sessions_router
from .chat.endpoint import router as chat_router

router = APIRouter()
router.include_router(agent_router, prefix="/agent", tags=["Agent"])
router.include_router(sessions_router, prefix="/sessions", tags=["Sessions"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])
router.include_router(health_router, prefix="/health", tags=["Health"])
