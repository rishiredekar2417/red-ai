from app.indexer.models import IndexedFile


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

        scored: list[tuple[int, IndexedFile]] = []

        for file in files:

            score = self.score_file(
                file,
                words,
            )

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