from pathlib import Path
from unittest.mock import patch

from app.llm.service import LLMService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@patch("app.llm.ollama_client.requests.post")
def test_history_adds_user_message(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "Hello back!",
        "model": "qwen2.5-coder:7b"
    }

    service = LLMService(PROJECT_ROOT)

    service.chat("Hello")

    assert len(service.history.all()) == 1


@patch("app.llm.ollama_client.requests.post")
def test_history_role(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "Hello back!",
        "model": "qwen2.5-coder:7b"
    }

    service = LLMService(PROJECT_ROOT)

    service.chat("Hello")

    assert service.history.all()[0].role == "user"


@patch("app.llm.ollama_client.requests.post")
def test_history_content(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "Hello back!",
        "model": "qwen2.5-coder:7b"
    }

    service = LLMService(PROJECT_ROOT)

    service.chat("Hello")

    assert service.history.all()[0].content == "Hello"