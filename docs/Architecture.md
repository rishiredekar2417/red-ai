# RED AI Architecture

## Vision

RED AI is an AI operating system for software engineering.

It is designed to:

- Understand entire codebases.
- Plan changes before editing.
- Ask permission before making modifications.
- Support multiple AI providers.
- Work locally or in the cloud.

## Core Principles

1. Provider Agnostic
2. Permission First
3. Modular Architecture
4. Test Driven
5. Secure by Default

## Layers

Frontend

↓

API

↓

Conversation

↓

Planner

↓

Memory

↓

Tools

↓

Providers

↓

Models

## Incremental Indexing Pipeline

The knowledge layer maintains a persisted project index that is refreshed incrementally rather than rebuilt from scratch on every run.

1. The workspace scanner discovers source files and ignores generated or internal folders.
2. The index builder compares each file with cached metadata such as path, size, and modification time.
3. New files are indexed, changed files are re-indexed, unchanged files are skipped, and deleted files are removed from the persisted index.
4. The stored index keeps chunk data and metadata so search and retrieval can consume a compact, persistent representation without rebuilding everything each time.

### Vector Storage and Lifecycle

- Vectors are generated per-chunk (function/class) during incremental indexing and stored in `knowledge/chunk_vectors.json`.
- Each vector entry includes metadata: `path`, `name`, `start_line`, `end_line`, and a deterministic `chunk_hash` computed from the chunk content.
- During indexing the system:
	- Validates the persisted vector DB on load and recovers corrupted entries.
	- Generates vectors only for chunks belonging to files that are newly added or detected as modified.
	- Detects renamed symbols by comparing `chunk_hash` values and re-uses existing vectors when content hash matches (rename without content change).
	- Removes vectors for deleted files and deleted chunks that no longer appear in the project index.
	- Persists vector updates atomically alongside the project index to keep them synchronized.

This design minimizes embedding work for large repositories by only regenerating vectors for changed chunks and re-using existing vectors where possible.

## Reranking and Retrieval

The retrieval pipeline performs an initial keyword-based search to identify candidate files and then extracts code `chunks` (functions, classes) from those files. A lightweight reranker then re-scores chunk candidates across files to prioritize exact symbol-name matches and higher-overlap content before building the final context sent to the model. This hybrid approach keeps retrieval fast while improving precision for symbol-heavy queries.

## Hybrid Retrieval Engine (new)

The Hybrid Retrieval Engine consolidates multiple retrieval strategies into a single ranked candidate list using Reciprocal Rank Fusion (RRF). Each strategy produces its own ordered candidate list; the merger combines them robustly while respecting explicit priority rules.

Retrieval strategies:
- Keyword search: token-overlap and filename scoring across the persisted `IndexedFile` objects.
- AST symbol search: exact match on function/class names (strong signal).
- Function/Class name search: partial name matches and heuristics.
- File path / filename search: match on path or filename tokens.
- Chunk relevance: TF-IDF-like re-ranking across candidate chunks for finer-grained relevance.
- Vector similarity: nearest-neighbor hits from the local `chunk_vectors.json` when available.
- Import relationships: files that import the queried symbol are surfaced as related hits.

Ranking and priority:
- Each strategy supplies a ranked list (best-first). We apply Reciprocal Rank Fusion (RRF) to merge lists: RRF sums 1/(k+rank) across sources for each candidate, giving robust aggregation and reducing sensitivity to any one source's score scale.
- We apply small deterministic boosts to exact symbol matches and to chunk-level results (prefer chunks over whole-file fallbacks).
- Priority rules are enforced by using exact-match boosts and by ordering candidate types: exact function/class match, filename match, keyword match, import relation, vector similarity, then whole-file fallback.

Context selection:
- After RRF merging we de-duplicate results (path+symbol+start_line+end_line) and enforce a token budget to select the highest-value chunks.
- We preserve related chunks from the same file when they provide additional context and fit the token budget.
- A content-based file fallback is used for queries that match raw file contents but do not match through the index metadata.

Performance and measurements:
- Retrieval latency and ranking latency are measured in benchmarks; the hybrid engine is designed to reuse lightweight keyword primitives and only call the vector store for the top-K vector candidates.
- RRF merging is O(N) in the number of candidates and sources; the implementation keeps K small (configurable) to bound CPU work.

Limitations and next steps:
- The current vector provider is a deterministic prototype; replacing it with a batched, async provider will change latency characteristics and should be integrated with the RRF pipeline.
- Persistence is JSON-backed and not atomic for very large indexes; migrating to an atomic local store (SQLite/LMDB) is recommended as a next milestone.

This hybrid design improves recall for semantic queries while preserving the precision and determinism required for symbol-aware developer tooling.