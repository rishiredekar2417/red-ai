from pathlib import Path

from app.knowledge.scanner import ProjectScanner
from .base import BaseTool


class SearchCodeTool(BaseTool):

    name = "search_code"

    description = "Search indexed project files by keyword."

    def __init__(self, root: Path):
        self.scanner = ProjectScanner(root)

    def execute(self, query: str, **kwargs):

        results = self.scanner.search(query)

        return [
            {
                "path": item.path,
                "language": item.language,
                "functions": item.functions,
                "classes": item.classes,
                "imports": item.imports,
            }
            for item in results
        ]