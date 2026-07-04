from pathlib import Path

from app.agent.orchestrator import AgentOrchestrator

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_list_tool():

    agent = AgentOrchestrator(PROJECT_ROOT)

    response = agent.run("list all files")

    assert response.success


def test_unknown_tool():

    agent = AgentOrchestrator(PROJECT_ROOT)

    response = agent.run("tell me a joke")

    assert not response.success
