from app.knowledge.scanner import ProjectScanner


class ContextSelector:

    def __init__(self, scanner: ProjectScanner):
        self.scanner = scanner

    def select(self, prompt: str):

        matches = self.scanner.search(prompt)

        python_files = []

        other_files = []

        for file in matches:

            if file.language == "Python":
                python_files.append(file)
            else:
                other_files.append(file)

        return (python_files + other_files)[:8]