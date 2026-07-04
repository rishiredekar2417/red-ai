from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RED AI"
    APP_VERSION: str = "0.1.0"

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    PROVIDER: str = "ollama"

    AI_PROVIDER: str = "ollama"

    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5-coder:7b"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5.5"

    TEMPERATURE: float = 0.2
    MAX_TOKENS: int = 4000

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()