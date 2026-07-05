class ContextSummarizer:

    MAX_LINES = 150

    def summarize(
        self,
        documents: list[str],
    ):

        sections = []

        for index, document in enumerate(documents, start=1):

            lines = document.splitlines()

            shortened = "\n".join(
                lines[: self.MAX_LINES]
            )

            sections.append(
                f"""
========================
DOCUMENT {index}
========================

{shortened}
"""
            )

        return "\n".join(sections)