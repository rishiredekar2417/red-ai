from pathlib import Path
from app.tools.registry import registry
from app.tools.manager import ToolManager

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_registry():
    manager = ToolManager(PROJECT_ROOT)

    assert registry.get("read_file") is not None

    assert registry.get("list_files") is not None


def test_registry_count():
    manager = ToolManager(PROJECT_ROOT)

    assert len(registry.all()) >= 2