from pydantic import BaseModel


class CodeChunk(BaseModel):
    path: str
    name: str
    type: str
    start_line: int
    end_line: int
    content: str
    score: int = 0