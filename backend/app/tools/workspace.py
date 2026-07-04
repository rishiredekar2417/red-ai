from pathlib import Path

from app.workspace.scanner import WorkspaceScanner
from .base import BaseTool


class WorkspaceTool(BaseTool):

    name = "workspace"
    description = "Scan the workspace and return all files."

    def __init__(self, root: Path):
        self.scanner = WorkspaceScanner(root)

    def execute(self, **kwargs):

        files = self.scanner.scan()

        return [
            {
                "path": file.path,
                "name": file.name,
                "extension": file.extension,
                "size": file.size,
            }
            for file in files
        ]