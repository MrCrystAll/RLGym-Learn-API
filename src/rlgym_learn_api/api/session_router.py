from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from rlgym_learn_api.api.services import get_session_service
from rlgym_learn_api.core.session_service import SessionService
from rlgym_learn_api.desc.session import Session
from rlgym_learn_api.desc.session_crud_schemas import (
    SessionGetAllArgs,
    SessionGetHealth,
    SessionSetSpacesArgs,
    SessionStartArgs,
)

router = APIRouter(prefix="/sessions", tags=["session"])


@router.post("/start", operation_id="start_new_session")
def start_new_session(
    args: SessionStartArgs,
    session_service: Annotated[SessionService, Depends(get_session_service)],
) -> Session:

    try:
        return session_service.start_session(args.project_id, args.run_name, args.port)
    except ValueError as e:
        return Response(str(e), 404)


@router.post("/{session_id}/stop", operation_id="stop_session")
def stop_session(
    session_id: str,
    session_service: Annotated[SessionService, Depends(get_session_service)],
) -> None:
    try:
        return session_service.stop_session(session_id)
    except ValueError as e:
        return Response(str(e), 404)


@router.post("/all", operation_id="get_all_sessions")
def get_all_sessions(
    args: SessionGetAllArgs,
    session_service: Annotated[SessionService, Depends(get_session_service)],
) -> list[Session]:
    try:
        return session_service.get_all_sessions(args.project_id, args.run_name)
    except FileNotFoundError as e:
        return Response(str(e), 404)
    except NotADirectoryError as e:
        return Response(str(e), 417)


@router.post("/{session_id}/health", operation_id="get_session_health")
def get_session_health(
    session_id: str,
    args: SessionGetHealth,
    session_service: Annotated[SessionService, Depends(get_session_service)],
) -> str:
    return session_service.get_session_health(
        args.project_id, args.run_name, session_id
    )


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
