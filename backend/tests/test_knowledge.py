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

    search = ProjectSearch()

    results = search.search(files, "test")

    assert len(results) > 0


def test_search_function():

    scanner = ProjectScanner(PROJECT_ROOT)

    files = scanner.scan()

    search = ProjectSearch()

    results = search.search(files, "scan")

    assert isinstance(results, list)
    assert len(results) > 0