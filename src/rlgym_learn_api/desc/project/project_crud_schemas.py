import os

from pydantic import BaseModel, Field

from rlgym_learn_api.desc.project.project import AdvancedConfigModel


class ProjectCreationArgs(BaseModel):
    # Name to create the project (Required)
    name: str
    advanced_config: AdvancedConfigModel = Field(default_factory=AdvancedConfigModel)


class ProjectUpdateRoot(BaseModel):
    path: str


class ProjectUpdateMetadata(BaseModel):
    name: str | None = None
    interpreter: str | os.PathLike[str] | None = None
