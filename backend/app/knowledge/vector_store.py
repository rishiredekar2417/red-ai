"""Lightweight in-memory vector store with optional JSON persistence.
"""
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class VectorStore:
    def __init__(self):
        # id -> vector
        self.vectors: Dict[str, List[float]] = {}
        # id -> metadata
        self.meta: Dict[str, Dict[str, Any]] = {}

    def add(self, id: str, vector: List[float], metadata: Optional[Dict[str, Any]] = None):
        self.vectors[id] = vector
        self.meta[id] = metadata or {}

    def remove(self, id: str):
        if id in self.vectors:
            del self.vectors[id]
        if id in self.meta:
            del self.meta[id]

    def find_by_chunk_hash(self, chunk_hash: str) -> Optional[str]:
        for id, m in self.meta.items():
            if m.get("chunk_hash") == chunk_hash:
                return id
        return None

    def find_by_path_and_start(self, path: str, start_line: int) -> Optional[str]:
        for id, m in self.meta.items():
            if m.get("path") == path and int(m.get("start_line") or -1) == int(start_line):
                return id
        return None

    def validate(self, dim: int) -> Tuple[List[str], List[str]]:
        """Validate stored vectors against expected dimension.

        Returns (valid_ids, corrupted_ids)
        """
        valid = []
        corrupted = []
        for id, vec in list(self.vectors.items()):
            try:
                if not isinstance(vec, list) or len(vec) != dim:
                    corrupted.append(id)
                    self.remove(id)
                    continue
                # ensure numeric
                for v in vec:
                    if not isinstance(v, (float, int)):
                        raise ValueError()
                valid.append(id)
            except Exception:
                corrupted.append(id)
                self.remove(id)

        return valid, corrupted

    def _cosine(self, v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        n1 = math.sqrt(sum(a * a for a in v1)) or 1.0
        n2 = math.sqrt(sum(b * b for b in v2)) or 1.0
        return dot / (n1 * n2)

    def query(self, vector: List[float], top_k: int = 5) -> List[Tuple[str, float, Dict[str, Any]]]:
        scores = []
        for id, vec in self.vectors.items():
            score = self._cosine(vector, vec)
            scores.append((id, score, self.meta.get(id, {})))

        scores.sort(key=lambda t: t[1], reverse=True)
        return scores[:top_k]

    def save(self, path: Path):
        data = {
            "vectors": self.vectors,
            "meta": self.meta,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def load(self, path: Path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.vectors = {k: v for k, v in data.get("vectors", {}).items()}
        self.meta = {k: v for k, v in data.get("meta", {}).items()}
