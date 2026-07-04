from app.core.config import PROVIDER

# from app.ai.providers.openai_provider import OpenAIProvider
from .ollama_provider import OllamaProvider


class ProviderFactory:

    @staticmethod
    def create():

        if PROVIDER == "openai":
            return OllamaProvider()
            # return OpenAIProvider()

        raise ValueError(
            f"Unknown provider: {PROVIDER}"
        )