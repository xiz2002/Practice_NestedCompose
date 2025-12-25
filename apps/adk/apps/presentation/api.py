from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .router.routers import router as root_router


app = FastAPI()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

app.include_router(root_router, prefix="/api/v1")
