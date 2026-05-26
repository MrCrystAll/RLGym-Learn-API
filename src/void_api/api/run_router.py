import json
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from rlgym_learn_algos.ppo.ppo_agent_controller import PPOAgentControllerConfigModel

from void_api.api.services import get_run_service
from void_api.core.run_service import RunService
from void_api.desc.run import Run
from void_api.desc.run_crud_schemas import RunCreationArgs, RunDeletionArgs

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("/create", operation_id="create_run")
def create_run(
    args: RunCreationArgs, run_service: Annotated[RunService, Depends(get_run_service)]
) -> None:
    try:
        run_service.create_run(args.project_id, args.run_name)
    except FileExistsError as e:
        return Response(str(e), status_code=409)  # Conflict
    except ValueError as e:
        return Response(str(e), status_code=404)  # Not found


@router.get("/all", operation_id="get_all_runs")
def get_all_runs(
    project_id: str, run_service: Annotated[RunService, Depends(get_run_service)]
) -> list[Run]:
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


@router.put("/{project_id}/{run_name}/config", operation_id="update_run_config")
async def update_run_config(
    project_id: str,
    run_name: str,
    request: Request,
    run_service: Annotated[RunService, Depends(get_run_service)],
):
    raw = await request.body()
    _raw_config = json.loads(raw)

    try:
        run_service.update_run_data(project_id, run_name, _raw_config)
    except AssertionError as e:
        return Response(str(e), status_code=400)


@router.post("/{project_id}/{run_name}/metrics", include_in_schema=False)
def update_metrics(
    project_id: str,
    run_name: str,
    metrics: dict[str, Any],
    run_service: Annotated[RunService, Depends(get_run_service)],
):
    return JSONResponse(
        {
            "reason": "TODO: Implement metrics",
            "data": metrics,
            "project_id": project_id,
            "run_name": run_name,
        },
        status_code=501,
    )


@router.delete("", operation_id="delete_run")
def delete_run(
    args: RunDeletionArgs, run_service: Annotated[RunService, Depends(get_run_service)]
) -> None:
    try:
        run_service.delete_run(args.project_id, args.run_name)
    except (FileNotFoundError, ValueError) as e:
        return Response(str(e), 404)  # Not found
    except OSError as e:
        return Response(str(e), 417)  # Invalid arguments


@router.get("/{project_id}/{run_name}/default", operation_id="get_default_config")
def get_default_config(
    project_id: str,
    run_name: str,
    config_type: str,
    run_service: Annotated[RunService, Depends(get_run_service)],
) -> PPOAgentControllerConfigModel:
    print(project_id, run_name, config_type)
    try:
        return run_service.get_default_config(project_id, run_name, config_type)
    except ValueError as e:
        return Response(str(e), 404)
