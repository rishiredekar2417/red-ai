from app.conversation.history import ConversationHistory


def test_add_message():

    history = ConversationHistory()

    history.add("user", "Hello")

    assert len(history.all()) == 1


def test_clear_history():

    history = ConversationHistory()

    history.add("user", "Hello")
    history.clear()

    assert len(history.all()) == 0


def test_message_order():

    history = ConversationHistory()

    history.add("user", "Hello")
    history.add("assistant", "Hi")

    messages = history.all()

    assert messages[0].role == "user"
    assert messages[1].role == "assistant"