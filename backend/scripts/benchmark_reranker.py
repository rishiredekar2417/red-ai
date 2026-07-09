import sys
import time
from statistics import mean
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.knowledge.search import ProjectSearch
from app.indexer.models import CodeChunk


def make_chunks(n, term="helper", density=0.1):
    chunks = []
    for i in range(n):
        # Some chunks include the term many times, some none
        if i % int(1 / max(density, 0.01)) == 0:
            content = (term + " ") * (10 + (i % 5))
            name = f"{term}_{i}"
        else:
            content = "some other content without the keyword " * 5
            name = f"fn_{i}"

        chunks.append(
            CodeChunk(
                name=name,
                kind="function",
                start_line=1,
                end_line=10,
                content=content,
            )
        )

    return chunks


def run_benchmark():
    search = ProjectSearch()

    sizes = [100, 500, 1000]
    for size in sizes:
        chunks = make_chunks(size, term="helper", density=0.05)
        # warmup
        search.rank_chunks(chunks, "helper")

        runs = 10
        times = []
        for _ in range(runs):
            t0 = time.perf_counter()
            ranked = search.rank_chunks(chunks, "helper")
            t1 = time.perf_counter()
            times.append(t1 - t0)

        print(f"Size={size:4d} avg_time={mean(times):.6f}s min={min(times):.6f}s max={max(times):.6f}s")
        print("Top 5 chunks:", [c.name for c in ranked[:5]])
        print("-")


if __name__ == '__main__':
    run_benchmark()
