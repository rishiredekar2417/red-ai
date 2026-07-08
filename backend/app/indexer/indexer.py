from pathlib import Path

from .filters import SUPPORTED_LANGUAGES
from .models import IndexedFile, CodeChunk
from .parser import PythonParser


class ProjectIndexer:

    def __init__(self):

        self.python = PythonParser()

    def index_file(self, file: Path):

        language = SUPPORTED_LANGUAGES.get(file.suffix, "Unknown")

        functions = []
        classes = []
        imports = []

        function_chunks = []
        class_chunks = []

        lines = 0

        if language == "Python":

            result = self.python.parse(file)

            functions = result["functions"]
            classes = result["classes"]
            imports = result["imports"]
            lines = result["lines"]

            function_chunks = [
                CodeChunk(**chunk)
                for chunk in result.get("function_chunks", [])
            ]

            class_chunks = [
                CodeChunk(**chunk)
                for chunk in result.get("class_chunks", [])
            ]

        return IndexedFile(
            path=str(file),
            language=language,
            size=file.stat().st_size,
            lines=lines,
            functions=functions,
            classes=classes,
            imports=imports,
            function_chunks=function_chunks,
            class_chunks=class_chunks,
        )