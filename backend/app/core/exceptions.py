class RedAIException(Exception):
    pass


class ToolNotFound(RedAIException):
    pass


class ProviderError(RedAIException):
    pass


class WorkspaceError(RedAIException):
    pass