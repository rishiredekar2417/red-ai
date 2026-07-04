from pathlib import Path

from .filters import SUPPORTED_LANGUAGES
from .models import IndexedFile
from .parser import PythonParser


class ProjectIndexer:

    def __init__(self):

        self.python = PythonParser()

    def index_file(self, file: Path):

        language = SUPPORTED_LANGUAGES.get(file.suffix, "Unknown")

        functions = []
        classes = []
        imports = []
        lines = 0

        if language == "Python":

            result = self.python.parse(file)

            functions = result["functions"]
            classes = result["classes"]
            imports = result["imports"]
            lines = result["lines"]

        return IndexedFile(
            path=str(file),
            language=language,
            size=file.stat().st_size,
            lines=lines,
            functions=functions,
            classes=classes,
            imports=imports,
        )
