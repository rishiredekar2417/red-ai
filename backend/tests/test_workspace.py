from pathlib import Path

from app.workspace.scanner import WorkspaceScanner

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_workspace_scan():
    scanner = WorkspaceScanner(PROJECT_ROOT)

    files = scanner.scan()

    assert len(files) > 0


def test_python_files_exist():
    scanner = WorkspaceScanner(PROJECT_ROOT)

    files = scanner.scan()

    assert any(file.extension == ".py" for file in files)
