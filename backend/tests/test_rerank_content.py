from app.knowledge.search import ProjectSearch
from app.indexer.models import CodeChunk


def test_rank_chunks_uses_content_tfidf():
    search = ProjectSearch()

    # Chunk with repeated query term in content
    chunk_heavy = CodeChunk(
        name="other",
        kind="function",
        start_line=1,
        end_line=10,
        content="""
def x():
    helper helper helper helper helper
    helper helper
""",
    )

    # Chunk with single occurrence only in name
    chunk_name = CodeChunk(
        name="helper",
        kind="function",
        start_line=20,
        end_line=30,
        content="no occurrence here",
    )

    ranked = search.rank_chunks([chunk_name, chunk_heavy], "helper")

    # content-heavy chunk should rank above name-only when many occurrences
    assert ranked[0].name == "other"
