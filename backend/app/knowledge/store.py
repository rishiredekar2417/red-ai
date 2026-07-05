import json
from pathlib import Path


class KnowledgeStore:

    def __init__(self, root: Path):

        self.root = Path(root).resolve()

        self.path = self.root / "knowledge" / "project_index.json"

    def exists(self) -> bool:

        return self.path.exists()

    def load(self):

        if not self.exists():
            return []

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def save(self, data):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )