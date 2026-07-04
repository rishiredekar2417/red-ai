from pathlib import Path


class ProjectSearch:

    def __init__(self, files):
        self.files = files

    def by_language(self, language):

        return [
            file
            for file in self.files
            if file.language == language
        ]

    def by_function(self, name):

        return [
            file
            for file in self.files
            if name in file.functions
        ]

    def by_class(self, name):

        return [
            file
            for file in self.files
            if name in file.classes
        ]

    def by_filename(self, name):

        return [
            file
            for file in self.files
            if Path(file.path).name == name
        ]