from pathlib import Path
from unittest.mock import patch
from app.llm.service import LLMService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@patch("app.llm.ollama_client.requests.post")
def test_ollama_chat_flow(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "response": "Hello from mock!",
        "model": "qwen2.5-coder:7b"
    }

    service = LLMService(PROJECT_ROOT)
    response = service.chat("Say hello in one sentence.")

    assert response.message == "Hello from mock!"
    assert response.model == "qwen2.5-coder:7b"