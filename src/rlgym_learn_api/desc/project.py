from pydantic import BaseModel


class ProjectMetadata(BaseModel):
    name: str
    id: str
    interpreter: str
