from .registry import registry


def tool(cls):

    instance = cls()

    registry.register(instance)

    return cls