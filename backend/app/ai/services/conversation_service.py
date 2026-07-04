from typing import List, Dict


class ConversationService:

    def __init__(self):
        self.messages: List[Dict[str, str]] = []

    def add_user(self, text: str):

        self.messages.append(
            {
                "role": "user",
                "content": text
            }
        )

    def add_assistant(self, text: str):

        self.messages.append(
            {
                "role": "assistant",
                "content": text
            }
        )

    def history(self):

        return self.messages