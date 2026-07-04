import json
from pathlib import Path


class ProjectCache:

    def __init__(self, file: Path):
        self.file = file

    def save(self, data):

        self.file.write_text(
            json.dumps(data, indent=4)
        )

    def load(self):

        if not self.file.exists():
            return []

        return json.loads(
            self.file.read_text()
        )