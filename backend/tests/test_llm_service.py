from pathlib import Path
from unittest.mock import patch

from app.core.settings import settings
from app.llm.service import LLMService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@patch("app.llm.ollama_client.requests.post")
def test_service(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "Explain details here",
        "model": settings.OLLAMA_MODEL
    }

    service = LLMService(PROJECT_ROOT)

    response = service.chat("Explain the project")

    assert response.model == settings.OLLAMA_MODEL


@patch("app.llm.ollama_client.requests.post")
def test_service_message(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "Hello back!",
        "model": settings.OLLAMA_MODEL
    }

    service = LLMService(PROJECT_ROOT)

    response = service.chat("Hello")

    assert isinstance(response.message, str)
    assert len(response.message) > 0