from pathlib import Path

from app.tools.manager import ToolManager

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_list_files():
    manager = ToolManager(PROJECT_ROOT)

    files = manager.execute("list_files")

    assert len(files) > 0


def test_read_file():
    manager = ToolManager(PROJECT_ROOT)

    content = manager.execute(
        "read_file",
        path=__file__,
    )

    assert "ToolManager" in content
