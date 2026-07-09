from pathlib import Path
from app.knowledge.index_builder import IndexBuilder
from app.context.retriever import ContextRetriever


def test_vector_augmented_retrieval(tmp_path: Path):
    # prepare a tiny project
    proj = tmp_path / "proj"
    proj.mkdir()
    src = proj / "sample.py"
    src.write_text("""
def foo():
    return 'foo value'

class Bar:
    def method(self):
        return 'bar'
""")

    # build index (will create chunk_vectors.json)
    builder = IndexBuilder(proj)
    builder.build(force=True)

    # ensure vectors file exists
    vec_path = proj / "knowledge" / "chunk_vectors.json"
    assert vec_path.exists()

    # run retriever with a query that should match the 'foo' function
    retriever = ContextRetriever(proj)
    docs = retriever.retrieve("foo")

    # at least one document should be returned and mention 'foo'
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert any("foo" in (d.get("symbol") or "").lower() or "foo" in (d.get("content") or "").lower() for d in docs)
