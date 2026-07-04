from pathlib import Path

from app.tools.manager import ToolManager


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_manager():
    manager = ToolManager(PROJECT_ROOT)

    assert manager is not None