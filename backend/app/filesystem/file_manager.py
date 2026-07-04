from pathlib import Path

from .permissions import PermissionManager


class FileManager:

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root).resolve()
        self.permissions = PermissionManager(self.project_root)

    def read(self, path: Path) -> str:
        file = self.permissions.validate(path)

        if not file.exists():
            raise FileNotFoundError(file)

        if file.is_dir():
            raise IsADirectoryError(file)

        return file.read_text(encoding="utf-8")

    def exists(self, path: Path) -> bool:
        file = self.permissions.validate(path)
        return file.exists()

    def list_directory(self, path: Path):
        directory = self.permissions.validate(path)

        if not directory.is_dir():
            raise NotADirectoryError(directory)

        return list(directory.iterdir())
