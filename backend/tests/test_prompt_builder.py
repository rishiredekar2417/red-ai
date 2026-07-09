from pathlib import Path

from app.llm.prompt_builder import PromptBuilder


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_prompt_contains_question():

    builder = PromptBuilder(PROJECT_ROOT)

    prompt = builder.build("Explain this project")

    assert "Explain this project" in prompt


def test_prompt_contains_context():

    builder = PromptBuilder(PROJECT_ROOT)

    prompt = builder.build("Explain")

    assert "PROJECT CONTEXT" in prompt
    assert "Relevant Chunks" in prompt