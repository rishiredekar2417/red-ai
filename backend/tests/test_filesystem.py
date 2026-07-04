from pathlib import Path

from app.filesystem.file_manager import FileManager

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_read_current_file():
    manager = FileManager(PROJECT_ROOT)

    current_file = Path(__file__)

    content = manager.read(current_file)

    assert "FileManager" in content


def test_file_exists():
    manager = FileManager(PROJECT_ROOT)

    assert manager.exists(Path(__file__))
