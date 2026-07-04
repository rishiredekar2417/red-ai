class ProjectGraph:

    def __init__(self):

        self.nodes = {}

    def add(self, indexed_file):

        self.nodes[indexed_file.path] = indexed_file

    def all_files(self):

        return list(self.nodes.values())

    def count(self):

        return len(self.nodes)