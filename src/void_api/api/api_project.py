from pydantic import BaseModel

from void_api.primitives import ProjectMetadata

class ProjectEntrypointStartArgs(BaseModel, extra="forbid"):
    metadata: ProjectMetadata
