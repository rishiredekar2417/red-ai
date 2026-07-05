from pathlib import Path

from app.core.settings import settings
from app.llm.service import LLMService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_service():

    service = LLMService(PROJECT_ROOT)

    response = service.chat("Explain the project")

    assert response.model == settings.OLLAMA_MODEL


def test_service_message():

    service = LLMService(PROJECT_ROOT)

    response = service.chat("Hello")

    assert isinstance(response.message, str)
    assert len(response.message) > 0