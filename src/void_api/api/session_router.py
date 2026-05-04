from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from void_api.api.services import get_session_service
from void_api.core.session_service import SessionService
from void_api.desc.session_crud_schemas import (
    SessionGetAllArgs,
    SessionSetSpacesArgs,
    SessionStartArgs,
)

router = APIRouter(prefix="/sessions", tags=["session"])


@router.post("/start")
def start_new_session(
    args: SessionStartArgs,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):

    try:
        return session_service.start_session(args.project_id, args.run_name)
    except ValueError as e:
        return Response(str(e), 404)


@router.post("/{session_id}/stop")
def stop_session(
    session_id: str,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    try:
        session_service.stop_session(session_id)
    except ValueError as e:
        return Response(str(e), 404)


@router.post("/all")
def get_all_sessions(
    args: SessionGetAllArgs,
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    try:
        return session_service.get_all_sessions(args.project_id, args.run_name)
    except FileNotFoundError as e:
        return Response(str(e), 404)
    except NotADirectoryError as e:
        return Response(str(e), 417)


@router.post("/{session_id}/metrics", include_in_schema=False)
def update_metrics(
    session_id: str,
    metrics: dict[str, Any],
    session_service: Annotated[SessionService, Depends(get_session_service)],
):
    return JSONResponse(
        {
            "reason": "TODO: Implement metrics",
            "data": metrics,
            "session_id": session_id,
        },
        status_code=501,
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
