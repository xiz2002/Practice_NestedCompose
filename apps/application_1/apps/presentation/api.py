from fastapi import FastAPI
from .router.routers import router as root_router


app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Welcome to the Presentation App!"
    }

# Todo router inclusion
app.include_router(root_router, prefix="/api/v1")
