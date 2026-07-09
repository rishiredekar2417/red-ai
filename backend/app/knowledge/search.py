import math
from collections import Counter

from app.indexer.models import IndexedFile, CodeChunk


class ProjectSearch:
    """
    Responsible only for searching and ranking indexed files.

    ProjectScanner builds the index.
    ProjectSearch searches the index.
    """

    def search(
        self,
        files: list[IndexedFile],
        query: str,
    ) -> list[IndexedFile]:

        words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        # optional vector hybrid support
        vector_scores = {}
        if hasattr(self, "vector_store") and self.vector_store and hasattr(self, "embedding_provider") and self.embedding_provider:
            qvec = self.embedding_provider.embed(query)
            # ask vector store for many candidates
            top = self.vector_store.query(qvec, top_k=max(10, len(getattr(self.vector_store, "vectors", {}))))
            for id, score, meta in top:
                path = meta.get("path")
                if path:
                    vector_scores[path] = score

        scored: list[tuple[int, IndexedFile]] = []

        for file in files:

            score = self.score_file(
                file,
                words,
            )

            # combine with vector score if available
            if vector_scores:
                score += int(vector_scores.get(file.path, 0) * 50)

            if score > 0:
                scored.append((score, file))

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            file
            for _, file in scored
        ]

    def retrieve_chunks(
        self,
        file: IndexedFile,
        query: str,
    ) -> list[CodeChunk]:
        words = {
            word.lower()
            for word in query.split()
            if len(word) > 2
        }

        scored: list[tuple[int, CodeChunk]] = []

        for chunk in file.chunks:
            score = self.score_chunk(chunk, words)
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [chunk for _, chunk in scored]

    def rank_chunks(
        self,
        chunks: list[CodeChunk],
        query: str,
    ) -> list[CodeChunk]:
        # TF-IDF-like re-ranking across the provided chunk set.
        terms = [w.lower() for w in query.split() if len(w) > 2]
        if not terms:
            return chunks

        # document frequency per term
        df = Counter()
        docs_tokens = []
        for chunk in chunks:
            tokens = [t.lower() for t in (chunk.name + " " + chunk.content).split() if len(t) > 2]
            docs_tokens.append(tokens)
            unique = set(tokens)
            for t in unique:
                df[t] += 1

        N = max(1, len(chunks))

        scored: list[tuple[float, CodeChunk]] = []

        for chunk, tokens in zip(chunks, docs_tokens):
            token_counts = Counter(tokens)
            score = 0.0

            # name match boost (moderate)
            name = chunk.name.lower()
            for term in terms:
                if term in name:
                    score += 2.0

            # TF-IDF over chunk text (amplified so many occurrences matter)
            for term in terms:
                tf = token_counts.get(term, 0)
                if tf == 0:
                    continue
                idf = math.log(1 + (N / (1 + df.get(term, 0))))
                score += (tf * idf) * 3.0

            # small kind match bonus
            for term in terms:
                if term in chunk.kind.lower():
                    score += 0.5

            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored]

    def score_chunk(
        self,
        chunk: CodeChunk,
        words: set[str],
    ) -> int:
        text = f"{chunk.name} {chunk.kind} {chunk.content}".lower()
        score = 0

        for word in words:
            if word in text:
                score += 20

        if any(word in chunk.name.lower() for word in words):
            score += 40

        if any(word in chunk.kind.lower() for word in words):
            score += 10

        if chunk.content:
            content_words = {
                word.lower()
                for word in chunk.content.split()
                if len(word) > 2
            }
            overlap = len(words & content_words)
            score += overlap * 8

        return score

    def score_file(
        self,
        file: IndexedFile,
        words: set[str],
    ) -> int:

        score = 0

        path = file.path.lower()
        language = file.language.lower()

        # ---------- filename ----------

        for word in words:

            if word in path:
                score += 30

        # ---------- language ----------

        for word in words:

            if word in language:
                score += 3

        # ---------- classes ----------

        for cls in file.classes:

            text = cls.lower()

            for word in words:

                if word in text:
                    score += 25

        # ---------- functions ----------

        for func in file.functions:

            text = func.lower()

            for word in words:

                if word in text:
                    score += 20

        # ---------- imports ----------

        for imp in file.imports:

            text = imp.lower()

            for word in words:

                if word in text:
                    score += 10

        return score