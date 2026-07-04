from pathlib import Path

from app.filesystem.file_manager import FileManager
from app.knowledge.scanner import ProjectScanner

from .models import Context
from .selector import ContextSelector
from .summarizer import ContextSummarizer


class ContextBuilder:

    def __init__(self, root: Path):

        self.files = FileManager(root)

        self.scanner = ProjectScanner(root)

        self.selector = ContextSelector(
            self.scanner
        )

        self.summarizer = ContextSummarizer()

    def build(self, prompt: str):

        matches = self.selector.select(prompt)

        paths = []

        docs = []

        for item in matches:

            paths.append(item.path)

            try:
                docs.append(
                    self.files.read(item.path)
                )

            except Exception:
                continue

        summary = self.summarizer.summarize(
            docs
        )

        return Context(
            prompt=prompt,
            files=paths,
            content=summary,
        )