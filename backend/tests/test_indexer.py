from pathlib import Path

from app.indexer.indexer import ProjectIndexer


def test_python_index():

    indexer = ProjectIndexer()

    file = Path(__file__)

    result = indexer.index_file(file)

    assert result.language == "Python"

    assert result.lines > 0
