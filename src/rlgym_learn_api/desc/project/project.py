from pydantic import BaseModel


class ProjectMetadata(BaseModel):
    name: str
    id: str
    interpreter: str
    created_at_version: str
