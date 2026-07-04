from pydantic import BaseModel


class IndexedFile(BaseModel):
    path: str
    language: str
    size: int
    lines: int
    functions: list[str]
    classes: list[str]
    imports: list[str]
