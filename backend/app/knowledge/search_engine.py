from pathlib import Path

from app.indexer.models import IndexedFile


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

            # Highest priority → filename
            for word in words:
                if word == filename:
                    score += 25

            # Classes
            for cls in file.classes:
                for word in words:
                    if word in cls.lower():
                        score += 20

            # Functions
            for func in file.functions:
                for word in words:
                    if word in func.lower():
                        score += 18

            # Imports
            for imp in file.imports:
                for word in words:
                    if word in imp.lower():
                        score += 10

            # Path
            lower_path = file.path.lower()

            for word in words:
                if word in lower_path:
                    score += 8

            # Language
            if file.language.lower() in words:
                score += 3

            if score > 0:
                matches.append((score, file))

        matches.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            file
            for _, file in matches
        ]