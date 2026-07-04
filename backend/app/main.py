from fastapi import FastAPI

from app.api.routes import router
from app.core.settings import settings
from app.core.logging import app_logger
from app.api.chat import router as chat_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RED AI Backend API"
)


@app.on_event("startup")
async def startup_event():
    app_logger.info(f"{settings.APP_NAME} Started Successfully")


@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info(f"{settings.APP_NAME} Shutdown")


app.include_router(router)
app.include_router(chat_router)