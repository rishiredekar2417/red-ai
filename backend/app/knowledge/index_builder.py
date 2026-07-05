from pathlib import Path

from app.indexer.indexer import ProjectIndexer
from app.knowledge.store import KnowledgeStore
from app.workspace.scanner import WorkspaceScanner


class IndexBuilder:

    def __init__(self, root: Path):

        self.root = Path(root).resolve()

        self.workspace = WorkspaceScanner(self.root)

        self.indexer = ProjectIndexer()

        self.store = KnowledgeStore(self.root)

    def build(self):

        index = []

        for workspace_file in self.workspace.scan():

            indexed = self.indexer.index_file(
                Path(workspace_file.path)
            )

            index.append(
                {
                    "path": indexed.path,
                    "language": indexed.language,
                    "size": indexed.size,
                    "lines": indexed.lines,
                    "functions": indexed.functions,
                    "classes": indexed.classes,
                    "imports": indexed.imports,
                }
            )

        self.store.save(index)

        return index