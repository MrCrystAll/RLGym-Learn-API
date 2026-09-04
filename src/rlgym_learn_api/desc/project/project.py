import os

from pydantic import BaseModel, Field


class AdvancedConfigModel(BaseModel):
    """Optional config the user can tweak at project creation"""

    # Whether the user handles their own venv
    user_handled_venv: bool = False

class ProjectMetadata(BaseModel):
    name: str
    id: str
    interpreter: str | os.PathLike[str] | None
    created_at_version: str

    advanced_config: AdvancedConfigModel = Field(default_factory=AdvancedConfigModel)
