from pydantic import BaseModel


class Context(BaseModel):
    prompt: str
    files: list[str]
    content: str