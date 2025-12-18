from fastapi import APIRouter
from .todo.todo import router as todo_router
from .health.health import router as health_router

router = APIRouter()
router.include_router(todo_router, tags=["Todo"])
router.include_router(health_router, tags=["Health"])
