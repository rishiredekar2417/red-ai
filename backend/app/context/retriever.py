from pathlib import Path

from app.filesystem.file_manager import FileManager
from app.indexer.models import CodeChunk, IndexedFile
from app.knowledge.scanner import ProjectScanner
from app.knowledge.search import ProjectSearch
from app.knowledge.vector_store import VectorStore
from app.knowledge.embeddings import EmbeddingProvider
from pathlib import Path
from collections import defaultdict
from typing import List


class ContextRetriever:

    MAX_DOCUMENTS = 5
    MAX_FILE_SIZE = 20000  # characters
    MAX_CONTEXT_TOKENS = 1800

    def __init__(self, root: Path):

        self.files = FileManager(root)
        self.scanner = ProjectScanner(root)
        self.search = ProjectSearch()

        # try to load persisted chunk vectors for vector-augmented retrieval
        self.vector_store = VectorStore()
        self.embedding_provider = EmbeddingProvider(dim=32)
        vec_path = Path(root) / "knowledge" / "chunk_vectors.json"
        if vec_path.exists():
            try:
                self.vector_store.load(vec_path)
            except Exception:
                self.vector_store = VectorStore()

        # RRF parameter (k) - larger k reduces influence of rank, tuned empirically
        self.rrf_k = 60

    def retrieve(self, prompt: str):
        # Audit the project index
        indexed_files: List[IndexedFile] = self.scanner.scan()

        # Each retrieval strategy returns a ranked list of document dicts
        sources = []
        sources.append(self._keyword_results(indexed_files, prompt))
        sources.append(self._symbol_results(indexed_files, prompt))
        sources.append(self._name_results(indexed_files, prompt))
        sources.append(self._path_results(indexed_files, prompt))
        sources.append(self._import_results(indexed_files, prompt))
        sources.append(self._vector_results(prompt))

        # Merge sources using Reciprocal Rank Fusion (RRF)
        merged = self._merge_rrf(sources, k=self.rrf_k)

        # If no merged candidates, try a simple content-based file fallback
        if not merged:
            for f in indexed_files:
                try:
                    content = self.files.read(f.path)
                    if prompt.lower() in content.lower():
                        merged = [self._doc_from_file(f, source="content_fallback", rank=1)]
                        break
                except Exception:
                    continue

        # Final de-dup, prioritize exact symbol matches and chunk types
        deduped = []
        seen = set()
        for doc in merged:
            key = f"{doc.get('path')}:{doc.get('symbol')}:{doc.get('start_line')}:{doc.get('end_line')}"
            if key in seen:
                continue
            seen.add(key)
            deduped.append(doc)
            if len(deduped) >= self.MAX_DOCUMENTS * 3:
                break

        # Enforce token budget and prefer same-file grouping heuristics
        final = self._apply_token_budget(deduped[: self.MAX_DOCUMENTS * 5])

        return final

    def _trim_chunk(self, content: str) -> str:
        return content.strip()

    def _score_chunk(self, chunk: CodeChunk, indexed_file) -> int:
        return 40 + (len(chunk.content.split()) // 4)

    def _score_file(self, indexed_file) -> int:
        return (
            len(indexed_file.functions) * 3
            + len(indexed_file.classes) * 3
            + len(indexed_file.imports)
        )

    def _chunk_key(self, chunk: CodeChunk, path: str) -> str:
        return f"{path}:{chunk.name}:{chunk.kind}:{chunk.start_line}:{chunk.end_line}"

    def _apply_token_budget(self, documents: list[dict]) -> list[dict]:
        budgeted = []
        used = 0
        for document in documents:
            estimated_tokens = max(1, len(document["content"].split()))
            if used + estimated_tokens > self.MAX_CONTEXT_TOKENS:
                break
            budgeted.append(document)
            used += estimated_tokens
        return budgeted

    # ----------------------- Helpers -----------------------
    def _doc_from_chunk(self, chunk: CodeChunk, f: IndexedFile, source: str = "", rank: int = 0, exact: bool = False) -> dict:
        return {
            "path": f.path,
            "symbol": chunk.name,
            "chunk_type": "chunk",
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
            "content": self._trim_chunk(chunk.content),
            "source": source,
            "rank": rank,
            "exact": exact,
        }

    def _doc_from_file(self, f: IndexedFile, source: str = "", rank: int = 0) -> dict:
        try:
            content = self.files.read(f.path)
            if len(content) > self.MAX_FILE_SIZE:
                content = content[: self.MAX_FILE_SIZE] + "\n\n... FILE TRUNCATED ..."
        except Exception:
            content = ""
        return {
            "path": f.path,
            "symbol": None,
            "chunk_type": "file",
            "start_line": 1,
            "end_line": None,
            "content": content,
            "source": source,
            "rank": rank,
            "exact": False,
        }

    # ----------------------- Retrieval sources -----------------------
    def _keyword_results(self, indexed_files: List[IndexedFile], prompt: str) -> list:
        files = self.search.search(indexed_files, prompt)
        results = []
        for rank, f in enumerate(files, start=1):
            chunks = self.search.retrieve_chunks(f, prompt)
            if chunks:
                for c_rank, chunk in enumerate(chunks, start=1):
                    results.append(self._doc_from_chunk(chunk, f, source="keyword", rank=c_rank))
            else:
                results.append(self._doc_from_file(f, source="keyword", rank=rank))
        return results

    def _symbol_results(self, indexed_files: List[IndexedFile], prompt: str) -> list:
        term = prompt.strip()
        results = []
        for f in indexed_files:
            for cls in f.classes:
                if cls == term:
                    chunk = next((c for c in f.chunks if c.name == cls), None)
                    if chunk:
                        results.append(self._doc_from_chunk(chunk, f, source="symbol", rank=1, exact=True))
            for func in f.functions:
                if func == term:
                    chunk = next((c for c in f.chunks if c.name == func), None)
                    if chunk:
                        results.append(self._doc_from_chunk(chunk, f, source="symbol", rank=1, exact=True))
        return results

    def _name_results(self, indexed_files: List[IndexedFile], prompt: str) -> list:
        words = {w.lower() for w in prompt.split() if len(w) > 0}
        results = []
        for f in indexed_files:
            for chunk in f.chunks:
                name = (chunk.name or "").lower()
                if any(w in name for w in words):
                    results.append(self._doc_from_chunk(chunk, f, source="name", rank=1))
        return results

    def _path_results(self, indexed_files: List[IndexedFile], prompt: str) -> list:
        results = []
        for rank, f in enumerate(self.search.search(indexed_files, prompt), start=1):
            results.append(self._doc_from_file(f, source="path", rank=rank))
        return results

    def _import_results(self, indexed_files: List[IndexedFile], prompt: str) -> list:
        term = prompt.strip().lower()
        results = []
        for rank, f in enumerate(indexed_files, start=1):
            for imp in f.imports:
                if term in imp.lower() or term in f.path.lower():
                    chunk = f.chunks[0] if f.chunks else None
                    if chunk:
                        results.append(self._doc_from_chunk(chunk, f, source="import", rank=rank))
                    else:
                        results.append(self._doc_from_file(f, source="import", rank=rank))
                    break
        return results

    def _vector_results(self, prompt: str) -> list:
        results = []
        try:
            if hasattr(self.vector_store, "vectors") and self.vector_store.vectors:
                qvec = self.embedding_provider.embed(prompt)
                hits = self.vector_store.query(qvec, top_k=20)
                for rank, (_id, score, meta) in enumerate(hits, start=1):
                    chunk_text = ""
                    try:
                        content = self.files.read(meta.get("path"))
                        lines = content.splitlines()
                        start = int(meta.get("start_line") or 1)
                        end = int(meta.get("end_line") or len(lines))
                        if start <= end and start >= 1:
                            chunk_text = "\n".join(lines[start - 1 : end])
                    except Exception:
                        chunk_text = ""

                    results.append({
                        "path": meta.get("path"),
                        "symbol": meta.get("name"),
                        "chunk_type": "chunk",
                        "start_line": meta.get("start_line"),
                        "end_line": meta.get("end_line"),
                        "content": self._trim_chunk(chunk_text) if chunk_text else "",
                        "score": float(score),
                        "source": "vector",
                        "rank": rank,
                        "exact": False,
                    })
        except Exception:
            pass
        return results

    # ----------------------- Merge / ranking -----------------------
    def _merge_rrf(self, sources: list, k: int = 60) -> list:
        scores = defaultdict(float)
        docs_meta = {}

        for src in sources:
            for rank, doc in enumerate(src, start=1):
                key = f"{doc.get('path')}:{doc.get('symbol')}:{doc.get('start_line')}:{doc.get('end_line')}"
                scores[key] += 1.0 / (k + rank)
                if key not in docs_meta:
                    docs_meta[key] = dict(doc)

        merged = []
        for key, score in scores.items():
            meta = docs_meta.get(key, {})
            meta["rrf_score"] = score
            merged.append(meta)

        # small boosts: exact symbol matches and chunk preference
        def boost(doc):
            boost_val = 0.0
            if doc.get("exact"):
                boost_val += 0.0002
            if doc.get("chunk_type") == "chunk":
                boost_val += 0.0001
            return doc.get("rrf_score", 0.0) + boost_val

        merged.sort(key=boost, reverse=True)
        return merged