from app.memory.memory import ConversationMemory


def test_memory():

    memory = ConversationMemory()

    memory.add("user", "Hello")

    memory.add("assistant", "Hi")

    assert len(memory.history()) == 2


def test_clear():

    memory = ConversationMemory()

    memory.add("user", "Hello")

    memory.clear()

    assert len(memory.history()) == 0