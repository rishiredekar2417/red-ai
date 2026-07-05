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
                document["content"]
                for document in documents
            ]
        )

        return Context(
            prompt=user_prompt,
            files=files,
            content=summary,
        )