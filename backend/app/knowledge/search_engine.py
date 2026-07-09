from pathlib import Path

from app.indexer.models import IndexedFile, CodeChunk


class ProjectSearch:

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

        matches = []

        for file in files:

            score = 0

            path = Path(file.path)

            filename = path.stem.lower()

            for word in words:
                if word == filename:
                    score += 25

            for cls in file.classes:
                for word in words:
                    if word in cls.lower():
                        score += 20

            for func in file.functions:
                for word in words:
                    if word in func.lower():
                        score += 18

            for imp in file.imports:
                for word in words:
                    if word in imp.lower():
                        score += 10

            lower_path = file.path.lower()
            for word in words:
                if word in lower_path:
                    score += 8

            if file.language.lower() in words:
                score += 3

            if score > 0:
                matches.append((score, file))

        matches.sort(key=lambda item: item[0], reverse=True)
        return [file for _, file in matches]

    def retrieve_chunks(
        self,
        file: IndexedFile,
        query: str,
    ) -> list[CodeChunk]:
        words = {word.lower() for word in query.split() if len(word) > 2}
        scored: list[tuple[int, CodeChunk]] = []

        for chunk in file.chunks:
            score = 0
            text = f"{chunk.name} {chunk.kind} {chunk.content}".lower()
            for word in words:
                if word in text:
                    score += 20
            if score > 0:
                scored.append((score, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored]