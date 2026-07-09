from app.core.settings import settings
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAIProvider


class ProviderFactory:

    @staticmethod
    def create():
        provider = settings.AI_PROVIDER.lower() if settings.AI_PROVIDER else settings.PROVIDER.lower()

        if provider == "ollama":
            return OllamaProvider()

        if provider == "openai":
            return OpenAIProvider()

        raise ValueError(f"Unknown provider: {provider}")

