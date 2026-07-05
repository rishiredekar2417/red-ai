from abc import ABC, abstractmethod

from .models import ChatResponse


class BaseLLM(ABC):

    @abstractmethod
    def chat(self, prompt: str) -> ChatResponse:
        ...