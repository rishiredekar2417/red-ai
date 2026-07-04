from ollama import AsyncClient
from app.core.settings import settings


class OllamaProvider:

    def __init__(self):
        self.client = AsyncClient(host=settings.OLLAMA_HOST)

    async def chat(self, messages):

        response = await self.client.chat(
            model=settings.OLLAMA_MODEL,
            host=settings.OLLAMA_URL,
            messages=messages,
        )

        return {"text": response["message"]["content"]}
