from pathlib import Path


class PermissionManager:

    def __init__(self, root: str):
        self.root = Path(root).resolve()

    def validate(self, path: str):

        target = Path(path).resolve()

        if not str(target).startswith(str(self.root)):
            raise PermissionError("Access outside project folder is not allowed.")

        return target
