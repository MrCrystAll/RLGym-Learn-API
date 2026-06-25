import os

from pydantic import BaseModel


class ProjectMetadata(BaseModel):
    name: str
    id: str
    interpreter: str | os.PathLike[str] | None
    created_at_version: str
