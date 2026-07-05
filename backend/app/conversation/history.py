from .models import Message


class ConversationHistory:

    def __init__(self):
        self.messages = []

    def add(self, role: str, content: str):
        self.messages.append(
            Message(role, content)
        )

    def clear(self):
        self.messages.clear()

    def all(self):
        return self.messages