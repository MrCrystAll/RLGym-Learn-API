from fastapi import APIRouter, Request

from void_api.api.api_crud_primitives import ProjectConfigUpdateArgs, ProjectDeleteArgs, ProjectGetDataArgs, ProjectGetDataReturn, ProjectInterpreterUpdateArgs, ProjectUpdateArgs
from void_api.api.api_project import ProjectEntrypointStartArgs
from void_api.crud_operations import delete_project, get_project_details, get_project_learning_config, update_config, update_project, update_project_python_interpreter
from void_api.project_operations import start_entrypoint

router = APIRouter(prefix="/project")

@router.post("/getDetails")
def api_get_project_data(args: ProjectGetDataArgs) -> ProjectGetDataReturn:
    _project_data = get_project_details(args.metadata)
    _config = get_project_learning_config(args.metadata)
    return ProjectGetDataReturn(project_data=_project_data, config=_config)

@router.delete("/delete")
def api_delete_project(args: ProjectDeleteArgs):
    delete_project(args.metadata)

@router.put("/")
def api_update_project(args: ProjectUpdateArgs):
    update_project(args.metadata)
    
@router.put("/interpreter")
def api_update_project_interpreter(args: ProjectInterpreterUpdateArgs):
    update_project_python_interpreter(args.metadata, args.python_path)
    
@router.post("/start")
def api_start_entrypoint(args: ProjectEntrypointStartArgs):
    start_entrypoint(args.metadata)
    
@router.put("/config")
async def api_update_config(request: Request):
    raw = await request.body()
    print(raw)
    config = ProjectConfigUpdateArgs.model_validate_json(raw)
    
    update_config(config.metadata, config.config)