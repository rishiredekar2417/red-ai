import asyncio

import pytest

from app.ai.services.chat_service import ChatService
from app.core.exceptions import ProviderError


class FailingProvider:
    async def chat(self, messages):
        raise RuntimeError("provider down")


def test_chat_service_wraps_provider_errors(monkeypatch):
    monkeypatch.setattr(
        "app.ai.services.chat_service.ProviderFactory.create",
        lambda: FailingProvider(),
    )

    service = ChatService()

    with pytest.raises(ProviderError, match="provider down"):
        asyncio.run(service.chat("hello"))
