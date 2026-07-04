from app.agent.models import AgentAction


class Planner:

    def plan(self, prompt: str):

        prompt_lower = prompt.lower()

        if "read" in prompt_lower:

            return AgentAction(tool="read_file", arguments={})

        if "list" in prompt_lower:

            return AgentAction(tool="list_files", arguments={})

        return None
