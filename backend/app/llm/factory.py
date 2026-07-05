from app.core.settings import settings

from .ollama_client import OllamaClient
from .openai_client import OpenAIClient


class LLMFactory:

    @staticmethod
    def create():

        provider = settings.PROVIDER.lower()

        if provider == "ollama":
            return OllamaClient()

        if provider == "openai":
            return OpenAIClient()

        raise ValueError(
            f"Unsupported provider: {provider}"
        )