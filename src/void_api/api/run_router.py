from typing import Annotated

from fastapi import APIRouter, Depends, Response

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


@router.delete("/", operation_id="delete_run")
def delete_run(
    args: RunDeletionArgs, run_service: Annotated[RunService, Depends(get_run_service)]
):
    try:
        run_service.delete_run(args.project_id, args.run_name)
    except (FileNotFoundError, ValueError) as e:
        return Response(str(e), 404)  # Not found
    except OSError as e:
        return Response(str(e), 417)  # Invalid arguments
