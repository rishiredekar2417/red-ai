from pathlib import Path

from .ignore import IGNORE_FOLDERS, IGNORE_EXTENSIONS
from .models import WorkspaceFile


class WorkspaceScanner:

    def __init__(self, root: Path):
        self.root = Path(root).resolve()

    def scan(self):
        files = []

        for item in self.root.rglob("*"):

            if any(folder in item.parts for folder in IGNORE_FOLDERS):
                continue

            if item.is_dir():
                continue

            if item.suffix in IGNORE_EXTENSIONS:
                continue

            files.append(
                WorkspaceFile(
                    path=str(item),
                    name=item.name,
                    extension=item.suffix,
                    size=item.stat().st_size,
                )
            )

        return files