from openai import AsyncOpenAI

from app.ai.providers.base_provider import BaseProvider
from app.core.settings import settings


class OpenAIProvider(BaseProvider):

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def chat(self, messages):
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

        return {"text": response.choices[0].message.content, "raw": response}

