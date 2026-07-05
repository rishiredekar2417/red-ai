from pathlib import Path

from app.llm.service import LLMService

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_history_adds_user_message():

    service = LLMService(PROJECT_ROOT)

    service.chat("Hello")

    assert len(service.history.all()) == 1

def test_history_role():

    service = LLMService(PROJECT_ROOT)

    service.chat("Hello")

    assert service.history.all()[0].role == "user"

def test_history_content():

    service = LLMService(PROJECT_ROOT)

    service.chat("Hello")

    assert service.history.all()[0].content == "Hello"