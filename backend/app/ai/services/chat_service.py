from app.ai.providers.provider_factory import ProviderFactory
from app.ai.services.conversation_service import ConversationService
from app.core.exceptions import ProviderError


class ChatService:

    def __init__(self):

        self.provider = ProviderFactory.create()

        self.conversation = ConversationService()

    async def chat(self, prompt: str):

        self.conversation.add_user(prompt)

        try:
            response = await self.provider.chat(self.conversation.history())
        except Exception as exc:
            raise ProviderError(str(exc)) from exc

        text = response.get("text") if isinstance(response, dict) else str(response)
        if not text:
            raise ProviderError("Provider returned an empty response")

        self.conversation.add_assistant(text)

        return text
