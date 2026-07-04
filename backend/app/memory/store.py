import json
from pathlib import Path


class MemoryStore:

    def __init__(self, file: Path):
        self.file = file

    def save(self, messages):

        self.file.write_text(
            json.dumps(messages, indent=4)
        )

    def load(self):

        if not self.file.exists():
            return []

        return json.loads(
            self.file.read_text()
        )