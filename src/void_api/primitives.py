from pydantic import BaseModel

class ProjectMetadata(BaseModel):
    name: str
    description: str | None
    version: str
    id: str
    path: str | None = None
    
class ProjectData(BaseModel):
    rewards_files: list[str]
    entrypoint: str

class Project(BaseModel):
    metadata: ProjectMetadata
    data: ProjectData
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Project):
            return False
        return value.metadata.id == self.metadata.id