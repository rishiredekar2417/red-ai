class LLMError(Exception):
    """Base LLM exception."""


class ProviderError(LLMError):
    """Raised when an LLM provider fails."""


class ConfigurationError(LLMError):
    """Raised when LLM configuration is invalid."""