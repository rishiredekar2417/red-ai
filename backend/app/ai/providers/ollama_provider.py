from ollama import AsyncClient
from app.core.settings import settings
from app.ai.providers.base_provider import BaseProvider


class OllamaProvider(BaseProvider):

    def __init__(self):
        self.client = AsyncClient(host=settings.OLLAMA_URL)

    async def chat(self, messages):
        response = await self.client.chat(
            model=settings.OLLAMA_MODEL,
            messages=messages,
        )

        return {"text": response["message"]["content"]}

