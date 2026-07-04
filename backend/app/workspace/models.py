from pathlib import Path
from pydantic import BaseModel


class WorkspaceFile(BaseModel):
    path: str
    name: str
    extension: str
    size: int


class WorkspaceSummary(BaseModel):
    root: str
    total_files: int
    total_directories: int
