from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseProvider(ABC):
    """
    Base class for every AI provider.

    Every provider (OpenAI, Claude, Gemini, Ollama...)
    must implement this interface.
    """

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Send messages to the AI model.

        Returns a standardized response.
        """
        raise NotImplementedError

