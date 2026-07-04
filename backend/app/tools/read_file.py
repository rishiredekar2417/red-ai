from pathlib import Path

from app.filesystem.file_manager import FileManager
from .base import BaseTool


class ReadFileTool(BaseTool):

    name = "read_file"
    description = "Read the contents of a file."

    def __init__(self, root: Path):
        self.manager = FileManager(root)

    def execute(self, path: str, **kwargs):

        return self.manager.read(Path(path))