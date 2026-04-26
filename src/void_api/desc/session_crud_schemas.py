from pydantic import BaseModel


class SessionStartArgs(BaseModel):
    run_name: str
    project_id: str
    
class SessionGetAllArgs(BaseModel):
    run_name: str
    project_id: str