from pathlib import Path

from app.knowledge.index_builder import IndexBuilder


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():

    print("=" * 60)
    print("Building Project Index...")
    print("=" * 60)

    builder = IndexBuilder(PROJECT_ROOT)

    index = builder.build()

    print(f"\nIndexed {len(index)} files.")
    print("\nSaved to knowledge/project_index.json")


if __name__ == "__main__":
    main()