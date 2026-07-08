import json
from pathlib import Path


class KnowledgeStore:

    def __init__(self, root: Path):

        self.root = Path(root).resolve()

        self.path = (
            self.root
            / "knowledge"
            / "project_index.json"
        )

    def exists(self):

        return self.path.exists()

    def load(self):

        if not self.exists():
            return []

        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def save(self, data):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
            )