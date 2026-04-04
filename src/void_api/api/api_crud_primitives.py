from pydantic import BaseModel

from void_api.primitives import Project, ProjectData, ProjectMetadata

class ProjectCreationArgs(BaseModel, extra="forbid"):
    path: str
    metadata: ProjectMetadata
    
class ProjectCreationReturn(BaseModel, extra="forbid"):
    project: Project
    
class ProjectsFetchArgs(BaseModel, extra="forbid"):
    path: str
    
class ProjectsFetchReturn(BaseModel, extra="forbid"):
    projects: list[ProjectMetadata]
    
class ProjectGetDataArgs(BaseModel, extra="forbid"):
    metadata: ProjectMetadata
    
class ProjectGetDataReturn(BaseModel, extra="forbid"):
    project_data: ProjectData
    
class ProjectDeleteArgs(BaseModel, extra="forbid"):
    metadata: ProjectMetadata