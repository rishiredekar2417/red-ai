from pathlib import Path

from app.knowledge.index_builder import IndexBuilder
from app.context.retriever import ContextRetriever


def test_exact_symbol_query(tmp_path: Path):
    proj = tmp_path / "proj_exact"
    proj.mkdir()
    src = proj / "mod.py"
    src.write_text("""
def foo():
    return 'foo-val'

class Bar:
    def method(self):
        return 'bar-val'
""")

    builder = IndexBuilder(proj)
    builder.build(force=True)

    r = ContextRetriever(proj)
    docs = r.retrieve("foo")

    assert isinstance(docs, list)
    assert len(docs) > 0
    # top result should match exact symbol 'foo' either in symbol or content
    top = docs[0]
    assert "foo" in (top.get("symbol") or "") or "foo" in (top.get("content") or "")


def test_natural_language_query(tmp_path: Path):
    proj = tmp_path / "proj_nl"
    proj.mkdir()
    src = proj / "nl.py"
    src.write_text("""
def compute_sum(a, b):
    # compute the sum of two numbers
    return a + b
""")
    builder = IndexBuilder(proj)
    builder.build(force=True)

    r = ContextRetriever(proj)
    docs = r.retrieve("add two numbers")
    assert len(docs) > 0
    assert any("sum" in (d.get("symbol") or "") or "sum" in (d.get("content") or "") for d in docs)


def test_duplicate_removal_vector_and_keyword(tmp_path: Path):
    proj = tmp_path / "proj_dup"
    proj.mkdir()
    src = proj / "dup.py"
    src.write_text("""
def foo():
    return 'dup'
""")

    builder = IndexBuilder(proj)
    builder.build(force=True)

    r = ContextRetriever(proj)
    # force a query likely to hit both keyword and vector
    docs = r.retrieve("foo")

    # ensure no duplicate path+symbol+start_line entries
    seen = set()
    for d in docs:
        key = f"{d.get('path')}:{d.get('symbol')}:{d.get('start_line')}:{d.get('end_line')}"
        assert key not in seen
        seen.add(key)


def test_token_budget_trimming(tmp_path: Path):
    proj = tmp_path / "proj_budget"
    proj.mkdir()
    src = proj / "big.py"
    # create a very large chunk
    content = "def big():\n" + "    x = '" + ("longtext " * 1000) + "'\n    return x\n"
    src.write_text(content)

    builder = IndexBuilder(proj)
    builder.build(force=True)

    r = ContextRetriever(proj)
    # temporarily lower token budget
    r.MAX_CONTEXT_TOKENS = 50
    docs = r.retrieve("big")
    # ensure returned content tokens do not exceed budget
    total = sum(len(d.get("content", "").split()) for d in docs)
    assert total <= r.MAX_CONTEXT_TOKENS


def test_file_fallback_when_no_chunks(tmp_path: Path):
    proj = tmp_path / "proj_fallback"
    proj.mkdir()
    src = proj / "data.py"
    # a Python file with no functions/classes so indexer creates a file entry but no chunks
    # valid Python but no functions/classes
    src.write_text("# just a textual python file with no functions\nMSG = 'This is sample text for fallback testing'")

    # IndexBuilder will create an index entry even for files; run build
    builder = IndexBuilder(proj)
    builder.build(force=True)

    r = ContextRetriever(proj)
    docs = r.retrieve("textual")
    # should return at least one file fallback
    assert len(docs) > 0
    assert any(d.get("chunk_type") == "file" for d in docs)
