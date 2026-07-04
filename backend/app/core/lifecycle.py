from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("RED AI Started Successfully")

    yield

    logger.info("RED AI Shutdown")