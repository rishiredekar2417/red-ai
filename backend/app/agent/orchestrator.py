from pathlib import Path

from app.agent.executor import Executor
from app.agent.models import AgentResponse
from app.agent.planner import Planner


class AgentOrchestrator:

    def __init__(self, root: Path):

        self.planner = Planner()
        self.executor = Executor(root)

    def run(self, prompt: str):

        action = self.planner.plan(prompt)

        if action is None:

            return AgentResponse(success=False, response="No tool matched.")

        result = self.executor.execute(action)

        return AgentResponse(success=True, response=str(result))
