from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel
from void_api.api.services import get_run_service
from void_api.core.run_service import RunService
from void_api.desc.run_crud_schemas import RunCreationArgs, RunDeletionArgs

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("/create", operation_id="create_run")
def create_run(
    args: RunCreationArgs, run_service: Annotated[RunService, Depends(get_run_service)]
):
    try:
        run_service.create_run(args.project_id, args.run_name)
    except FileExistsError as e:
        return Response(str(e), status_code=409)  # Conflict
    except ValueError as e:
        return Response(str(e), status_code=404)  # Not found


@router.get("/all", operation_id="get_all_runs")
def get_all_runs(
    project_id: str, run_service: Annotated[RunService, Depends(get_run_service)]
):
    try:
        return run_service.get_all_runs(project_id)
    except ValueError as e:
        return Response(str(e), 404)


@router.post("/{project_id}/{run_name}/data", operation_id="get_run_data")
def get_run_data(
    project_id: str,
    run_name: str,
    run_service: Annotated[RunService, Depends(get_run_service)],
):
    try:
        return run_service.get_run_data(project_id, run_name)
    except OSError as e:
        return Response(content=str(e), status_code=404)
    except ValueError as e:
        return Response(content=str(e), status_code=417)


@router.put("/{project_id}/{run_name}/config", operation_id="update_project_config")
async def update_project_config(
    project_id: str,
    run_name: str,
    request: Request,
    run_service: Annotated[RunService, Depends(get_run_service)],
):
    raw = await request.body()
    config = LearningCoordinatorConfigModel.model_validate_json(raw)

    try:
        run_service.update_run_data(project_id, run_name, config)
    except AssertionError as e:
        return Response(str(e), status_code=400)


@router.get("/all", operation_id="get_all_projects")
@router.delete("", operation_id="delete_run")
def delete_run(
    args: RunDeletionArgs, run_service: Annotated[RunService, Depends(get_run_service)]
):
    try:
        run_service.delete_run(args.project_id, args.run_name)
    except (FileNotFoundError, ValueError) as e:
        return Response(str(e), 404)  # Not found
    except OSError as e:
        return Response(str(e), 417)  # Invalid arguments
