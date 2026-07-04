from pathlib import Path

from app.filesystem.file_manager import FileManager
from .base import BaseTool


class FilesystemTool(BaseTool):

    name = "filesystem"
    description = "Read a file from the workspace."

    def __init__(self, root: Path):
        self.manager = FileManager(root)

    def execute(self, path: str, **kwargs):

        return self.manager.read(Path(path))