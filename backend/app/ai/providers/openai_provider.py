from openai import AsyncOpenAI

from app.ai.providers.base_provider import BaseProvider
from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)
api_key=settings.OPENAI_API_KEY


class OpenAIProvider(BaseProvider):

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def chat(self, messages):

        response = await self.client.responses.create(
            model=OPENAI_MODEL, input=messages
        )

        return {"text": response.output_text, "raw": response}
