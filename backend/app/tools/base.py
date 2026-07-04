from abc import ABC, abstractmethod


class BaseTool(ABC):

    name: str = ""
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs):
        """Execute the tool."""
        pass

    def schema(self):
        return {
            "name": self.name,
            "description": self.description,
        }