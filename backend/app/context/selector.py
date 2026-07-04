from app.knowledge.scanner import ProjectScanner


class ContextSelector:

    def __init__(self, scanner: ProjectScanner):
        self.scanner = scanner

    def select(self, prompt: str):

        prompt = prompt.lower()

        matches = self.scanner.search(prompt)

        return matches[:5]