from pydantic import BaseModel


class FileInfo(BaseModel):
    path: str
    name: str
    size: int
    is_directory: bool
