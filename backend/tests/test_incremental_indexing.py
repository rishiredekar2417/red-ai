import json
import time
from pathlib import Path

import pytest

from app.knowledge.index_builder import IndexBuilder
from app.knowledge.store import KnowledgeStore


@pytest.fixture
def temp_project(tmp_path):
    project_root = tmp_path / "project"
    project_root.mkdir()
    (project_root / "knowledge").mkdir()
    return project_root


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_incremental_indexing_indexes_new_file(temp_project):
    builder = IndexBuilder(temp_project)
    write_file(temp_project / "example.py", "def hello():\n    return 1\n")

    summary = builder.build()

    assert summary["indexed"] == 1
    assert summary["updated"] == 0
    assert summary["removed"] == 0
    assert summary["skipped"] == 0

    store = KnowledgeStore(temp_project)
    data = store.load()
    assert len(data) == 1
    assert data[0]["path"].endswith("example.py")


def test_incremental_indexing_reindexes_modified_file(temp_project):
    builder = IndexBuilder(temp_project)
    write_file(temp_project / "example.py", "def hello():\n    return 1\n")
    builder.build()

    time.sleep(0.02)
    write_file(temp_project / "example.py", "def hello():\n    return 2\n")

    summary = builder.build()

    assert summary["updated"] == 1
    assert summary["indexed"] == 0


def test_incremental_indexing_removes_deleted_file(temp_project):
    builder = IndexBuilder(temp_project)
    write_file(temp_project / "example.py", "def hello():\n    return 1\n")
    builder.build()

    (temp_project / "example.py").unlink()

    summary = builder.build()

    assert summary["removed"] == 1


def test_incremental_indexing_skips_unchanged_file(temp_project):
    builder = IndexBuilder(temp_project)
    write_file(temp_project / "example.py", "def hello():\n    return 1\n")
    builder.build()

    summary = builder.build()

    assert summary["skipped"] == 1


def test_incremental_indexing_persists_cache_metadata(temp_project):
    builder = IndexBuilder(temp_project)
    write_file(temp_project / "example.py", "def hello():\n    return 1\n")
    builder.build()

    store = KnowledgeStore(temp_project)
    data = store.load()

    assert data[0]["mtime"] > 0
    assert data[0]["size"] > 0


def test_incremental_indexing_rebuilds_when_forced(temp_project):
    builder = IndexBuilder(temp_project)
    write_file(temp_project / "example.py", "def hello():\n    return 1\n")
    builder.build()

    summary = builder.build(force=True)

    assert summary["indexed"] == 1
    assert summary["updated"] == 0
    assert summary["removed"] == 0
    assert summary["skipped"] == 0
