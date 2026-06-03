import json
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from rlgym_learn_algos.ppo.ppo_agent_controller import PPOAgentControllerConfigModel

from rlgym_learn_api.api.services import get_run_service
from rlgym_learn_api.core.run_service import RunService
from rlgym_learn_api.desc.exception import (
    RLGymLearnApiException,
    RLGymLearnApiExceptionModel,
)
from rlgym_learn_api.desc.run.run import Run
from rlgym_learn_api.desc.run.run_crud_schemas import RunCreationArgs, RunDeletionArgs

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post(
    "/create",
    operation_id="create_run",
    responses={
        200: {"model": None},
        404: {"model": RLGymLearnApiExceptionModel},
        409: {"model": RLGymLearnApiExceptionModel},
    },
)
def create_run(
    args: RunCreationArgs, run_service: Annotated[RunService, Depends(get_run_service)]
):
    try:
        run_service.create_run(args.project_id, args.run_name)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), status_code=e.error_code)


@router.get(
    "/all",
    operation_id="get_all_runs",
    responses={200: {"model": list[Run]}, 404: {"model": RLGymLearnApiExceptionModel}},
)
def get_all_runs(
    project_id: str, run_service: Annotated[RunService, Depends(get_run_service)]
):
    try:
        return run_service.get_all_runs(project_id)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), status_code=e.error_code)


@router.post(
    "/{project_id}/{run_name}/data",
    operation_id="get_run_data",
    responses={
        200: {
            "model": None
        },  # Technically LearningCoordinatorConfigModel, but it's broken because of SerdesTypesModel
        404: {"model": RLGymLearnApiExceptionModel},
        417: {"model": RLGymLearnApiExceptionModel},
    },
)
def get_run_data(
    project_id: str,
    run_name: str,
    run_service: Annotated[RunService, Depends(get_run_service)],
):
    try:
        return run_service.get_run_data(project_id, run_name)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), status_code=e.error_code)


@router.put(
    "/{project_id}/{run_name}/config",
    operation_id="update_run_config",
    responses={
        200: {"model": None},
        404: {"model": RLGymLearnApiExceptionModel},
        417: {"model": RLGymLearnApiExceptionModel},
    },
)
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
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), status_code=e.error_code)


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


@router.delete(
    "",
    operation_id="delete_run",
    responses={200: {"model": None}, 404: {"model": RLGymLearnApiExceptionModel}},
)
def delete_run(
    args: RunDeletionArgs, run_service: Annotated[RunService, Depends(get_run_service)]
):
    try:
        run_service.delete_run(args.project_id, args.run_name)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), status_code=e.error_code)


@router.get(
    "/{project_id}/{run_name}/default",
    operation_id="get_default_config",
    responses={
        200: {"model": PPOAgentControllerConfigModel},
        417: {"model": RLGymLearnApiExceptionModel},
    },
)
def get_default_config(
    project_id: str,
    run_name: str,
    config_type: str,
    run_service: Annotated[RunService, Depends(get_run_service)],
):
    try:
        return run_service.get_default_config(project_id, run_name, config_type)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), status_code=e.error_code)
