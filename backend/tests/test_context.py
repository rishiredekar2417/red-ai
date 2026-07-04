from pathlib import Path

from app.context.builder import ContextBuilder

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_context_builder():

    builder = ContextBuilder(PROJECT_ROOT)

    context = builder.build("python")

    assert context.prompt == "python"


def test_context_contains_files():

    builder = ContextBuilder(PROJECT_ROOT)

    context = builder.build("python")

    assert isinstance(context.files, list)


def test_context_contains_content():

    builder = ContextBuilder(PROJECT_ROOT)

    context = builder.build("python")

    assert isinstance(context.content, str)