from app.tools.registry import registry


def test_registry():

    assert registry.get("read_file") is not None

    assert registry.get("list_files") is not None


def test_registry_count():

    assert len(registry.all()) >= 2