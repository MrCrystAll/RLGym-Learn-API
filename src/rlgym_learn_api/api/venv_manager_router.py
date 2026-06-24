from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from rlgym_learn_venv_manager.api.virtual_environment import VenvConfig

from rlgym_learn_api.api.services import get_venv_manager_service
from rlgym_learn_api.core.venv_manager_service import VenvManagerService
from rlgym_learn_api.desc.exception import (
    RLGymLearnApiException,
    RLGymLearnApiExceptionModel,
)
from rlgym_learn_api.desc.venv_manager.crud_operations import (
    VenvCreationArgs,
    VenvInstallArgs,
    VenvUpdateArgs,
)

router = APIRouter(prefix="/venv", tags=["venv"])


@router.post(
    "",
    responses={
        200: {"model": VenvConfig},
        500: {"model": RLGymLearnApiExceptionModel},
    },
    operation_id="create_venv",
)
def create_venv(
    args: VenvCreationArgs,
    venv_manager_service: Annotated[
        VenvManagerService, Depends(get_venv_manager_service)
    ],
):
    try:
        return venv_manager_service.create_venv(
            preset=args.preset,
            project_id=args.project_id,
            python_executable=args.python_executable,
        )
    except RLGymLearnApiException as e:
        return JSONResponse(content=e.to_dict().model_dump(), status_code=e.error_code)


@router.delete(
    "",
    responses={
        200: {"model": str},
        404: {"model": RLGymLearnApiExceptionModel},
        500: {"model": RLGymLearnApiExceptionModel},
    },
    operation_id="delete_venv",
)
def delete_venv(
    project_id: str,
    venv_manager_service: Annotated[
        VenvManagerService, Depends(get_venv_manager_service)
    ],
):
    try:
        venv_manager_service.delete_venv(project_id)
        return f"The virtual environment for the project {project_id} has been successfully deleted."
    except RLGymLearnApiException as e:
        return JSONResponse(content=e.to_dict().model_dump(), status_code=e.error_code)


@router.post(
    "/install",
    responses={
        200: {"model": str},
        404: {"model": RLGymLearnApiExceptionModel},
        409: {"model": RLGymLearnApiExceptionModel},
        500: {"model": RLGymLearnApiExceptionModel},
    },
    operation_id="install_package",
)
def install_package(
    args: VenvInstallArgs,
    venv_manager_service: Annotated[
        VenvManagerService, Depends(get_venv_manager_service)
    ],
):
    try:
        venv_manager_service.install(
            args.project_id, args.package_name, *args.extra_args
        )
        return f"The package {args.package_name} has been successfully installed."
    except RLGymLearnApiException as e:
        return JSONResponse(content=e.to_dict().model_dump(), status_code=e.error_code)


@router.get(
    "/package_update",
    responses={
        200: {"model": dict[str, str]},
        404: {"model": RLGymLearnApiExceptionModel},
        500: {"model": RLGymLearnApiExceptionModel},
    },
    operation_id="get_updatable_packages",
)
def get_updatable_packages(
    project_id: str,
    venv_manager_service: Annotated[
        VenvManagerService, Depends(get_venv_manager_service)
    ],
):
    try:
        return venv_manager_service.get_updatable_packages(project_id)
    except RLGymLearnApiException as e:
        return JSONResponse(content=e.to_dict().model_dump(), status_code=e.error_code)


@router.post(
    "/update",
    responses={
        200: {"model": str},
        404: {"model": RLGymLearnApiExceptionModel},
        500: {"model": RLGymLearnApiExceptionModel},
    },
    operation_id="update_package",
)
def update_package(
    args: VenvUpdateArgs,
    venv_manager_service: Annotated[
        VenvManagerService, Depends(get_venv_manager_service)
    ],
):
    try:
        venv_manager_service.update_package(args.project_id, args.package_name)
        return f"Package {args.package_name} has been updated successfully."
    except RLGymLearnApiException as e:
        return JSONResponse(content=e.to_dict().model_dump(), status_code=e.error_code)
