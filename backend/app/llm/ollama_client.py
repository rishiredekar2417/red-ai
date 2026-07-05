import requests

from app.core.settings import settings

from .base import BaseLLM
from .models import ChatResponse


class OllamaClient(BaseLLM):

    def __init__(self):

        self.url = f"{settings.OLLAMA_URL}/api/generate"

    def chat(self, prompt: str) -> ChatResponse:

        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=300,
            )

            response.raise_for_status()

            data = response.json()

            return ChatResponse(
                message=data["response"],
                model=data["model"],
            )

        except requests.exceptions.RequestException as e:

            return ChatResponse(
                message=f"Ollama connection error: {e}",
                model="error",
            )