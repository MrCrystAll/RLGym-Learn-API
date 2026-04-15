from pydantic import BaseModel

from void_api.primitives import Project, ProjectData, ProjectMetadata

from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel

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
    config: LearningCoordinatorConfigModel
    
class ProjectDeleteArgs(BaseModel, extra="forbid"):
    metadata: ProjectMetadata
    
class ProjectUpdateArgs(BaseModel, extra="forbid"):
    metadata: ProjectMetadata
    
class ProjectInterpreterUpdateArgs(BaseModel, extra="forbid"):
    metadata: ProjectMetadata
    python_path: str
    
class ProjectConfigUpdateArgs(BaseModel, extra="forbid"):
    metadata: ProjectMetadata
    config: LearningCoordinatorConfigModel