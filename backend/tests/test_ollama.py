from pathlib import Path

from app.llm.service import LLMService

PROJECT_ROOT = Path(__file__).resolve().parent.parent

service = LLMService(PROJECT_ROOT)

response = service.chat(
    "Say hello in one sentence."
)

print("\nMODEL:")
print(response.model)

print("\nRESPONSE:")
print(response.message)