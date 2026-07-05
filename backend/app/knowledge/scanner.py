from pathlib import Path

from app.workspace.scanner import WorkspaceScanner
from app.indexer.indexer import ProjectIndexer


class ProjectScanner:

    def __init__(self, root: Path):
        self.workspace = WorkspaceScanner(root)
        self.indexer = ProjectIndexer()

    def scan(self):

        indexed_files = []

        for workspace_file in self.workspace.scan():

            path = Path(workspace_file.path)

            indexed_files.append(
                self.indexer.index_file(path)
            )

        return indexed_files

    def search(self, query: str):

        words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        matches = []

        for file in self.scan():

            score = 0

            searchable = " ".join([
                file.path,
                file.language,
                " ".join(file.classes),
                " ".join(file.functions),
                " ".join(file.imports),
            ]).lower()

            for word in words:
                if word in searchable:
                    score += 1

            if score:
                matches.append((score, file))

        matches.sort(
            key=lambda x: x[0],
            reverse=True,
        )

        return [file for _, file in matches]