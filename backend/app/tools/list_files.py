from pathlib import Path

from app.workspace.scanner import WorkspaceScanner
from .base import BaseTool


class ListFilesTool(BaseTool):

    name = "list_files"
    description = "List every file in the workspace."

    def __init__(self, root: Path):
        self.scanner = WorkspaceScanner(root)

    def execute(self, **kwargs):

        files = self.scanner.scan()

        return [file.path for file in files]