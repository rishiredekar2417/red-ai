from pathlib import Path

from app.conversation.history import ConversationHistory

from .factory import LLMFactory
from .prompt_builder import PromptBuilder


class LLMService:

    def __init__(self, root: Path):

        self.history = ConversationHistory()

        self.prompt = PromptBuilder(root)

        self.client = LLMFactory.create()

    def chat(self, user_prompt: str):

        self.history.add(
            "user",
            user_prompt,
        )

        prompt = self.prompt.build(
            user_prompt,
            self.history.all(),
        )

        return self.client.chat(prompt)