from app.core.config import PROVIDER

from app.ai.providers.openai_provider import OpenAIProvider


class ProviderFactory:

    @staticmethod
    def create():

        if PROVIDER == "openai":
            return OpenAIProvider()

        raise ValueError(
            f"Unknown provider: {PROVIDER}"
        )