from pathlib import Path

from .registry import registry
from .list_files import ListFilesTool
from .read_file import ReadFileTool


class ToolManager:

    def __init__(self, root: Path):

        # Prevent duplicate registration
        if registry.get("list_files") is None:
            registry.register(ListFilesTool(root))

        if registry.get("read_file") is None:
            registry.register(ReadFileTool(root))

    def execute(
        self,
        name: str,
        **kwargs,
    ):

        tool = registry.get(name)

        if tool is None:
            raise ValueError(f"Unknown tool: {name}")

        return tool.execute(**kwargs)

    def available(self):

        return [
            tool.schema()
            for tool in registry.all()
        ]