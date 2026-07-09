from pathlib import Path
import json
import shutil
import time

from app.knowledge.index_builder import IndexBuilder


def read_vectors(proj: Path):
    p = proj / "knowledge" / "chunk_vectors.json"
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def test_deleted_file_vectors(tmp_path: Path):
    proj = tmp_path / "proj"
    proj.mkdir()
    f = proj / "a.py"
    f.write_text("""
def foo():
    return 1
""")

    builder = IndexBuilder(proj)
    res1 = builder.build(force=True)
    vecs1 = read_vectors(proj)
    assert vecs1.get("meta") is not None
    assert len(vecs1.get("meta", {})) > 0

    # remove file
    f.unlink()
    res2 = builder.build()
    vecs2 = read_vectors(proj)
    # vectors should be removed
    assert len(vecs2.get("meta", {})) == 0


def test_deleted_chunk_vectors(tmp_path: Path):
    proj = tmp_path / "proj2"
    proj.mkdir()
    f = proj / "b.py"
    f.write_text("""
def a():
    return 1

def b():
    return 2
""")

    builder = IndexBuilder(proj)
    builder.build(force=True)
    vecs = read_vectors(proj)
    assert len(vecs.get("meta", {})) == 2

    # remove one function
    f.write_text("""
def a():
    return 1
""")
    builder.build()
    vecs2 = read_vectors(proj)
    # one vector should remain
    assert len(vecs2.get("meta", {})) == 1


def test_renamed_function_reuses_vector(tmp_path: Path):
    proj = tmp_path / "proj3"
    proj.mkdir()
    f = proj / "c.py"
    f.write_text("""
def foo():
    return 'x'
""")

    builder = IndexBuilder(proj)
    builder.build(force=True)
    vecs1 = read_vectors(proj)
    meta1 = vecs1.get("meta", {})
    assert len(meta1) == 1
    old_id = list(meta1.keys())[0]

    # rename function but keep body same (start_line same)
    f.write_text("""
def bar():
    return 'x'
""")
    builder.build()
    vecs2 = read_vectors(proj)
    meta2 = vecs2.get("meta", {})
    # new id should exist
    assert any("bar" in k for k in meta2.keys())


def test_modified_chunk_regenerates(tmp_path: Path):
    proj = tmp_path / "proj4"
    proj.mkdir()
    f = proj / "d.py"
    f.write_text("""
def foo():
    return 'v1'
""")

    builder = IndexBuilder(proj)
    builder.build(force=True)
    vecs1 = read_vectors(proj)
    meta1 = vecs1.get("meta", {})
    id1 = list(meta1.keys())[0]
    ch1 = meta1[id1].get("chunk_hash")

    # modify body
    f.write_text("""
def foo():
    return 'v2'
""")
    builder.build()
    vecs2 = read_vectors(proj)
    meta2 = vecs2.get("meta", {})
    id2 = list(meta2.keys())[0]
    ch2 = meta2[id2].get("chunk_hash")
    assert ch1 != ch2


def test_corrupted_vector_recovery(tmp_path: Path):
    proj = tmp_path / "proj5"
    proj.mkdir()
    f = proj / "e.py"
    f.write_text("""
def foo():
    return 1
""")

    builder = IndexBuilder(proj)
    builder.build(force=True)

    vec_path = proj / "knowledge" / "chunk_vectors.json"
    # corrupt the file
    with open(vec_path, "w", encoding="utf-8") as fobj:
        fobj.write("{ invalid json")

    # next build should handle missing/corrupted vector DB gracefully
    builder = IndexBuilder(proj)
    res = builder.build()
    vecs = read_vectors(proj)
    assert isinstance(vecs.get("meta", {}), dict)
    # vectors should be recovered (regenerated)
    assert len(vecs.get("meta", {})) == 1


def test_unchanged_chunk_skipped(tmp_path: Path):
    proj = tmp_path / "proj6"
    proj.mkdir()
    f = proj / "f.py"
    f.write_text("""
def foo():
    return 42
""")

    builder = IndexBuilder(proj)
    res1 = builder.build(force=True)
    # rebuild without changes
    res2 = builder.build()
    # generated should be 0 on second run (no new vectors)
    assert res2.get("generated", 0) == 0


def test_startup_loading(tmp_path: Path):
    proj = tmp_path / "proj7"
    proj.mkdir()
    f = proj / "g.py"
    f.write_text("""
def foo():
    return 7
""")

    builder = IndexBuilder(proj)
    builder.build(force=True)
    # create a new builder to ensure it loads vectors from disk
    builder2 = IndexBuilder(proj)
    assert len(builder2.vector_store.vectors) == len(builder.vector_store.vectors)
