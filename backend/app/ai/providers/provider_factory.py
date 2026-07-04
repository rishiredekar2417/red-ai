from app.core.config import PROVIDER

# from app.ai.providers.openai_provider import OpenAIProvider
from .ollama_provider import OllamaProvider
from app.core.settings import settings

class ProviderFactory:

    @staticmethod
    def create():
        if settings.AI_PROVIDER == "ollama":
            return OllamaProvider()
    
        if settings.PROVIDER == "openai":
            return OpenAIProvider()

        if settings.PROVIDER == "lmstudio":
            return LMStudioProvider()

        if settings.PROVIDER == "anthropic":
            return ClaudeProvider()

        raise ValueError(f"Unknown provider: {PROVIDER}")
