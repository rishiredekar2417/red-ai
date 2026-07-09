# Reranking Benchmarks

This document describes the lightweight reranker benchmark harness included in the repository.

Location
- `backend/scripts/benchmark_reranker.py`

Purpose
- Generate synthetic `CodeChunk` sets with controlled term frequency and measure the `rank_chunks` latency and top-ranked symbols.

How to run
1. Activate the project's virtualenv and change to the `backend` folder.
2. Run:

```bash
python scripts/benchmark_reranker.py
```

What it measures
- Average, min, and max ranking latency for varying chunk set sizes.
- Example top-ranked symbol outputs to inspect qualitative behavior.

Notes
- The harness is intentionally simple; for larger-scale benchmarking consider using real source-derived chunks and a profiling tool.
