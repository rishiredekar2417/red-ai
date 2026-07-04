import ast
from pathlib import Path


class PythonParser:

    def parse(self, file: Path):

        source = file.read_text(encoding="utf-8", errors="ignore")

        tree = ast.parse(source)

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)

            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(source.splitlines()),
        }
