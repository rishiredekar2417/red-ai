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

        query = query.lower()

        matches = []

        for file in self.scan():

            # Match language
            if query in file.language.lower():
                matches.append(file)
                continue

            # Match file path
            if query in file.path.lower():
                matches.append(file)
                continue

            # Match function names
            if any(query in func.lower() for func in file.functions):
                matches.append(file)
                continue

            # Match class names
            if any(query in cls.lower() for cls in file.classes):
                matches.append(file)
                continue

            # Match imported modules
            if any(query in imp.lower() for imp in file.imports):
                matches.append(file)
                continue

        return matches