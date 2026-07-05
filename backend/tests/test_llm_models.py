from app.llm.models import ChatMessage, ChatResponse


def test_chat_message():

    msg = ChatMessage(
        role="user",
        content="Hello"
    )

    assert msg.role == "user"


def test_chat_response():

    response = ChatResponse(
        message="Hi",
        model="test"
    )

    assert response.model == "test"