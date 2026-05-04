from typing import Generic

from pydantic import BaseModel
from rlgym.api import ActionSpaceType, ObsSpaceType


class SessionStartArgs(BaseModel):
    run_name: str
    project_id: str


class SessionGetAllArgs(BaseModel):
    run_name: str
    project_id: str


class SessionSetSpacesArgs(BaseModel, Generic[ObsSpaceType, ActionSpaceType]):
    agent_controller_name: str
    obs_space: ObsSpaceType
    act_space: ActionSpaceType
