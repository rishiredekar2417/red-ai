from app.core.config import (
    APP_NAME,
    APP_VERSION,
    ENVIRONMENT,
    LOG_LEVEL,
    OPENAI_API_KEY,
)

class Settings:
    APP_NAME = APP_NAME
    APP_VERSION = APP_VERSION
    ENVIRONMENT = ENVIRONMENT
    LOG_LEVEL = LOG_LEVEL
    OPENAI_API_KEY = OPENAI_API_KEY

settings = Settings()