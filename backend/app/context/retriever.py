from pathlib import Path

from app.filesystem.file_manager import FileManager
from app.knowledge.scanner import ProjectScanner


class ContextRetriever:

    def __init__(self, root: Path):

        self.files = FileManager(root)
        self.scanner = ProjectScanner(root)

    def retrieve(self, prompt: str):

        matches = self.scanner.search(prompt)

        documents = []

        for match in matches:

            try:

                content = self.files.read(match.path)

                documents.append(
                    {
                        "path": match.path,
                        "content": content,
                        "score": len(match.functions)
                        + len(match.classes)
                        + len(match.imports),
                    }
                )

            except Exception:
                continue

        documents.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return documents[:5]