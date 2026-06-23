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
from rlgym_learn_api.desc.venv_manager.crud_operations import VenvCreationArgs

router = APIRouter(prefix="/venv", tags=["venv"])


@router.post(
    "",
    responses={
        200: {"model": VenvConfig},
        500: {"model": RLGymLearnApiExceptionModel},
    },
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
