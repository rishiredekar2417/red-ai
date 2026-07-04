from pathlib import Path

from app.agent.models import AgentAction
from app.tools.manager import ToolManager


class Executor:

    def __init__(self, root: Path):

        self.tools = ToolManager(root)

    def execute(self, action: AgentAction):

        return self.tools.execute(
            action.tool,
            **action.arguments,
        )