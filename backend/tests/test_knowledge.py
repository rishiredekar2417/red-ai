from pathlib import Path

from app.knowledge.scanner import ProjectScanner
from app.knowledge.search import ProjectSearch


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_scan():

    scanner = ProjectScanner(PROJECT_ROOT)

    files = scanner.scan()

    assert len(files) > 0


def test_search_python():

    scanner = ProjectScanner(PROJECT_ROOT)

    files = scanner.scan()

    search = ProjectSearch(files)

    python_files = search.by_language("Python")

    assert len(python_files) > 0


def test_search_function():

    scanner = ProjectScanner(PROJECT_ROOT)

    files = scanner.scan()

    search = ProjectSearch(files)

    assert isinstance(search.by_function("scan"), list)