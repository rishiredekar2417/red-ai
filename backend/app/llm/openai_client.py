from openai import OpenAI

from app.core.settings import settings

from .base import BaseLLM
from .models import ChatResponse


class OpenAIClient(BaseLLM):

    def __init__(self):

        self.client = None

        if settings.OPENAI_API_KEY:

            self.client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
            )

    def chat(self, prompt: str) -> ChatResponse:

        # No API key -> keep stub behavior
        if self.client is None:

            return ChatResponse(
                message="OpenAI client not connected yet.",
                model="stub",
            )

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

        return ChatResponse(
            message=response.choices[0].message.content,
            model=response.model,
        )