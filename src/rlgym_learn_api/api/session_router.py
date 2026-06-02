from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from rlgym_learn_api.api.services import get_session_service
from rlgym_learn_api.core.session_service import SessionService
from rlgym_learn_api.desc.exception import (
    RLGymLearnApiException,
    RLGymLearnApiExceptionModel,
)
from rlgym_learn_api.desc.session.exceptions import SessionNotFoundError
from rlgym_learn_api.desc.session.session import Session
from rlgym_learn_api.desc.session.session_crud_schemas import (
    SessionGetAllArgs,
    SessionGetHealth,
    SessionSetSpacesArgs,
    SessionStartArgs,
)

router = APIRouter(prefix="/sessions", tags=["session"])


@router.post(
    "/start",
    operation_id="start_new_session",
    responses={200: {"model": Session}, 404: {"model": RLGymLearnApiExceptionModel}},
)
def start_new_session(
    args: SessionStartArgs,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):

    try:
        return session_service.start_session(args.project_id, args.run_name, args.port)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), e.error_code)


@router.post(
    "/{session_id}/stop",
    operation_id="stop_session",
    responses={200: {"model": int}, 404: {"model": RLGymLearnApiExceptionModel}},
)
def stop_session(
    session_id: str,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    try:
        return session_service.stop_session(session_id)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), e.error_code)


@router.post(
    "/all",
    operation_id="get_all_sessions",
    responses={
        200: {"model": list[Session]},
        404: {"model": RLGymLearnApiExceptionModel},
        417: {"model": RLGymLearnApiExceptionModel},
    },
)
def get_all_sessions(
    args: SessionGetAllArgs,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    try:
        return session_service.get_all_sessions(args.project_id, args.run_name)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), e.error_code)


@router.post(
    "/{session_id}/health",
    operation_id="get_session_health",
    responses={200: {"model": str}, 404: {"model": RLGymLearnApiExceptionModel}},
)
def get_session_health(
    session_id: str,
    args: SessionGetHealth,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    try:
        return session_service.get_session_health(
            args.project_id, args.run_name, session_id
        )
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict().model_dump(), e.error_code)


@router.post("/{session_id}/spaces", include_in_schema=False)
def set_space_types(
    session_id: str,
    spaces: SessionSetSpacesArgs,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    return JSONResponse(
        {
            "reason": "TODO: Implement set spaces",
            "data": spaces.model_dump(),
            "session_id": session_id,
        },
        status_code=501,
    )
