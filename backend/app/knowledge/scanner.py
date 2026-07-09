from pathlib import Path

from app.indexer.indexer import ProjectIndexer
from app.indexer.models import IndexedFile
from app.knowledge.search_engine import ProjectSearch
from app.knowledge.store import KnowledgeStore
from app.workspace.scanner import WorkspaceScanner


class ProjectScanner:

    def __init__(self, root: Path):

        self.root = Path(root)

        self.workspace = WorkspaceScanner(root)

        self.indexer = ProjectIndexer()

        self.store = KnowledgeStore(root)

        self.search_engine = ProjectSearch()

    def scan(self):

        # Load cached index

        if self.store.exists():

            data = self.store.load()

            return [
                IndexedFile(**item)
                for item in data
            ]

        # Build new index

        indexed_files = []

        for workspace_file in self.workspace.scan():

            indexed_files.append(
                self.indexer.index_file(
                    Path(workspace_file.path)
                )
            )

        # Save

        self.store.save(
            [
                file.model_dump()
                for file in indexed_files
            ]
        )

        return indexed_files

    def search(
        self,
        query: str,
    ):

        from .search import ProjectSearch

        search_engine = ProjectSearch()

        return search_engine.search(
            self.scan(),
            query,
        )
    