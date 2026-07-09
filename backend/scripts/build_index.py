import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.knowledge.index_builder import IndexBuilder


def main():

    print("=" * 60)
    print("Rebuilding Project Index...")
    print("=" * 60)

    builder = IndexBuilder(PROJECT_ROOT)
    summary = builder.build(force=True)

    print(f"\nIndexed: {summary['indexed']} files")
    print(f"Updated: {summary['updated']} files")
    print(f"Skipped: {summary['skipped']} files")
    print(f"Removed: {summary['removed']} files")
    print(f"Total entries: {summary['total']}")
    print("\nSaved to knowledge/project_index.json")


if __name__ == "__main__":
    main()