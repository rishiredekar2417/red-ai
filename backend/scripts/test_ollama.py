from pathlib import Path

from app.llm.service import LLMService

# Project root (backend/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    print("=" * 80)
    print("RED AI - OLLAMA TEST")
    print("=" * 80)

    service = LLMService(PROJECT_ROOT)

    while True:
        print()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("\nGoodbye!")
            break

        print("\nThinking...\n")

        try:
            response = service.chat(user_input)

            print("=" * 80)
            print(f"MODEL : {response.model}")
            print("-" * 80)
            print(response.message)
            print("=" * 80)

        except Exception as e:
            print("\nERROR:")
            print(e)
            print()


if __name__ == "__main__":
    main()