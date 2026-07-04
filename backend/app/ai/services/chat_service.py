from app.ai.providers.provider_factory import ProviderFactory
from app.ai.services.conversation_service import ConversationService


class ChatService:

    def __init__(self):

        self.provider = ProviderFactory.create()

        self.conversation = ConversationService()

    async def chat(self, prompt: str):

        self.conversation.add_user(prompt)

        response = await self.provider.chat(
            self.conversation.history()
        )

        self.conversation.add_assistant(
            response["text"]
        )

        return response["text"]