from pydantic import BaseModel


class RunCreationArgs(BaseModel):
    run_name: str
    project_id: str


class RunDeletionArgs(BaseModel):
    run_name: str
    project_id: str
