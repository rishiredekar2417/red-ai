from pathlib import Path

from app.indexer.indexer import ProjectIndexer
from app.indexer.models import CodeChunk, IndexedFile
from app.knowledge.search import ProjectSearch


def test_chunk_retrieval_returns_relevant_chunks():
    indexer = ProjectIndexer()
    project_root = Path(__file__).resolve().parent.parent

    indexed = indexer.index_file(project_root / "app" / "indexer" / "parser.py")
    search = ProjectSearch()

    matches = search.retrieve_chunks(indexed, "parse")

    assert len(matches) > 0
    assert all(chunk.content for chunk in matches)


def test_chunk_retrieval_prefers_symbol_matches_over_plain_text():
    search = ProjectSearch()

    file = IndexedFile(
        path="/tmp/example.py",
        language="Python",
        size=100,
        lines=20,
        functions=["helper"],
        classes=["Parser"],
        imports=["os"],
        chunks=[
            CodeChunk(
                name="helper",
                kind="function",
                start_line=1,
                end_line=5,
                content="return value",
            ),
            CodeChunk(
                name="unused",
                kind="function",
                start_line=6,
                end_line=10,
                content="the query word appears many times in generic text",
            ),
        ],
        function_chunks=[
            CodeChunk(
                name="helper",
                kind="function",
                start_line=1,
                end_line=5,
                content="return value",
            )
        ],
        class_chunks=[],
    )

    matches = search.retrieve_chunks(file, "helper parser")

    assert matches[0].name == "helper"
