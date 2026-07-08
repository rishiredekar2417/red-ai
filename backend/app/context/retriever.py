from pathlib import Path

from app.filesystem.file_manager import FileManager
from app.knowledge.scanner import ProjectScanner


class ContextRetriever:

    MAX_DOCUMENTS = 5
    MAX_FILE_SIZE = 20000  # characters

    def __init__(self, root: Path):

        self.files = FileManager(root)
        self.scanner = ProjectScanner(root)

    def retrieve(self, prompt: str):

        matches = self.scanner.search(prompt)

        documents = []
        seen = set()

        for match in matches:

            if match.path in seen:
                continue

            seen.add(match.path)

            try:

                content = self.files.read(match.path)

                if len(content) > self.MAX_FILE_SIZE:
                    content = (
                        content[: self.MAX_FILE_SIZE]
                        + "\n\n... FILE TRUNCATED ..."
                    )

                score = (
                    len(match.functions) * 3
                    + len(match.classes) * 3
                    + len(match.imports)
                )

                documents.append(
                    {
                        "path": match.path,
                        "content": content,
                        "score": score,
                    }
                )

            except Exception:
                continue

        documents.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        return documents[: self.MAX_DOCUMENTS]