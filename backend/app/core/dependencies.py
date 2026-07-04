from app.ai.providers.provider_factory import ProviderFactory


def get_provider():
    return ProviderFactory.create()