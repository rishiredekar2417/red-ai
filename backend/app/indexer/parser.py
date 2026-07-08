import ast
from pathlib import Path


class PythonParser:

    def parse(self, file: Path):

        source = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        tree = ast.parse(source)

        lines = source.splitlines()

        functions = []
        classes = []
        imports = []

        function_chunks = []
        class_chunks = []

        for node in ast.walk(tree):

            # ---------------------------------
            # Functions
            # ---------------------------------

            if isinstance(node, ast.FunctionDef):

                functions.append(node.name)

                function_chunks.append(
                    {
                        "name": node.name,
                        "kind": "function",
                        "start_line": node.lineno,
                        "end_line": getattr(
                            node,
                            "end_lineno",
                            node.lineno,
                        ),
                        "content": "\n".join(
                            lines[
                                node.lineno - 1:
                                getattr(
                                    node,
                                    "end_lineno",
                                    node.lineno,
                                )
                            ]
                        ),
                    }
                )

            # ---------------------------------
            # Classes
            # ---------------------------------

            elif isinstance(node, ast.ClassDef):

                classes.append(node.name)

                class_chunks.append(
                    {
                        "name": node.name,
                        "kind": "class",
                        "start_line": node.lineno,
                        "end_line": getattr(
                            node,
                            "end_lineno",
                            node.lineno,
                        ),
                        "content": "\n".join(
                            lines[
                                node.lineno - 1:
                                getattr(
                                    node,
                                    "end_lineno",
                                    node.lineno,
                                )
                            ]
                        ),
                    }
                )

            # ---------------------------------
            # Imports
            # ---------------------------------

            elif isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                imports.append(
                    node.module or ""
                )

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "lines": len(lines),
            "function_chunks": function_chunks,
            "class_chunks": class_chunks,
        }