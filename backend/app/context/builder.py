from pathlib import Path

from .models import Context
from .retriever import ContextRetriever
from .summarizer import ContextSummarizer


class ContextBuilder:

    def __init__(self, root: Path):

        self.retriever = ContextRetriever(root)

        self.summarizer = ContextSummarizer()

    def build(
        self,
        user_prompt: str,
        history=None,
    ):

        documents = self.retriever.retrieve(user_prompt)

        files = [
            document["path"]
            for document in documents
        ]

        summary = self.summarizer.summarize(
            [
                self._format_document(document)
                for document in documents
            ]
        )

        return Context(
            prompt=user_prompt,
            files=files,
            content=summary,
        )

    def _format_document(self, document: dict) -> str:
        header = f"Path: {document['path']}"
        if document.get("symbol"):
            header += f"\nSymbol: {document['symbol']}"
            header += f"\nType: {document['chunk_type']}"
            header += f"\nLines: {document['start_line']}-{document['end_line']}"
        else:
            header += "\nType: file"
        return f"{header}\n\n{document['content']}"