from pathlib import Path

from app.knowledge.embeddings import EmbeddingProvider
from app.knowledge.vector_store import VectorStore


def test_vector_store_returns_most_similar():
    emb = EmbeddingProvider(dim=32)
    store = VectorStore()

    doc1 = "database connection pool and SQL queries"
    doc2 = "network socket communication and rpc"

    v1 = emb.embed(doc1)
    v2 = emb.embed(doc2)

    store.add("doc1", v1, {"path": "/tmp/doc1", "text": doc1})
    store.add("doc2", v2, {"path": "/tmp/doc2", "text": doc2})

    q = emb.embed("database queries")

    results = store.query(q, top_k=2)

    assert results[0][0] == "doc1"
