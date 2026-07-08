from pydantic import BaseModel


class CodeChunk(BaseModel):
    """
    A logical piece of code extracted from a source file.

    Usually a function, class, or module-level block.
    """

    name: str

    kind: str

    start_line: int

    end_line: int

    content: str