from app.knowledge.search import ProjectSearch
from app.indexer.models import IndexedFile
from app.knowledge.embeddings import EmbeddingProvider
from app.knowledge.vector_store import VectorStore


def test_hybrid_search_prefers_vector_match():
    emb = EmbeddingProvider(dim=32)
    store = VectorStore()

    # Build two fake indexed files
    file1 = IndexedFile(
        path="/tmp/db.py",
        language="Python",
        size=10,
        lines=10,
        functions=["connect"],
        classes=[],
        imports=["sqlalchemy"],
        chunks=[],
        function_chunks=[],
        class_chunks=[],
    )

    file2 = IndexedFile(
        path="/tmp/net.py",
        language="Python",
        size=10,
        lines=10,
        functions=["send"],
        classes=[],
        imports=["socket"],
        chunks=[],
        function_chunks=[],
        class_chunks=[],
    )

    # Add vectors keyed by arbitrary ids but with meta path matching file paths
    # Make doc_db vector equal to the query embedding to ensure it ranks highest
    store.add("doc_db", emb.embed("database queries"), {"path": file1.path})
    store.add("doc_net", emb.embed("socket network rpc"), {"path": file2.path})

    search = ProjectSearch()
    # attach vectorstore and embedding provider
    search.vector_store = store
    search.embedding_provider = emb

    results = search.search([file1, file2], "database queries")

    assert results[0].path == file1.path
