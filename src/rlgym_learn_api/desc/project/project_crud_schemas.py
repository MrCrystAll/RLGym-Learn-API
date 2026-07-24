import os

from pydantic import BaseModel


class ProjectCreationArgs(BaseModel):
    # Name to create the project (Required)
    name: str


class ProjectUpdateRoot(BaseModel):
    path: str


class ProjectUpdateMetadata(BaseModel):
    name: str | None = None
    interpreter: str | os.PathLike[str] | None = None
