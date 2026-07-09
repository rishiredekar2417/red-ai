"""Simple local embedding provider for prototyping.

Produces deterministic pseudo-embeddings using SHA256 hashing.
"""
import hashlib
import math
from typing import List


class EmbeddingProvider:
    def __init__(self, dim: int = 64):
        self.dim = dim

    def embed(self, text: str) -> List[float]:
        """Return a deterministic float vector for `text` of length `dim`.

        This is a lightweight stand-in for an external embedding model.
        """
        vec = [0.0] * self.dim
        if not text:
            return vec

        # Use a hashing trick to generate reproducible pseudo-random floats
        for i in range(self.dim):
            hasher = hashlib.sha256()
            hasher.update(text.encode("utf-8"))
            hasher.update(i.to_bytes(2, "little"))
            digest = hasher.digest()
            # Use first 8 bytes as integer
            val = int.from_bytes(digest[:8], "little", signed=False)
            # Map to [-1, 1)
            vec[i] = ((val / (2 ** 64)) * 2.0) - 1.0

        # Normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]
