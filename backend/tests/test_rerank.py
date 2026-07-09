from app.knowledge.search import ProjectSearch
from app.indexer.models import CodeChunk


def test_rank_chunks_prefers_name_matches():
    search = ProjectSearch()

    # Chunk where the query appears in the symbol name
    chunk_name = CodeChunk(
        name="helper",
        kind="function",
        start_line=1,
        end_line=5,
        content="some unrelated content",
    )

    # Chunk where the query only appears in the content
    chunk_content = CodeChunk(
        name="other",
        kind="function",
        start_line=10,
        end_line=20,
        content="this contains helper in the body text",
    )

    ranked = search.rank_chunks([chunk_content, chunk_name], "helper")

    assert len(ranked) == 2
    assert ranked[0].name == "helper"
