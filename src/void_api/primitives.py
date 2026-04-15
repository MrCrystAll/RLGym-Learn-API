from pydantic import BaseModel

class ProjectMetadata(BaseModel):
    name: str
    id: str
    path: str | None = None
    
class ProjectLogConfig(BaseModel):
    stdout_log: str
    
class ProjectData(BaseModel):
    rewards_files: list[str]
    entrypoint: str
    interpreter: str
    config_file: str
    
    log_config: ProjectLogConfig

class Project(BaseModel):
    metadata: ProjectMetadata
    data: ProjectData
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Project):
            return False
        return value.metadata.id == self.metadata.id