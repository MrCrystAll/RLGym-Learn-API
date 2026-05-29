from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from rlgym_learn_api.api.services import get_project_service
from rlgym_learn_api.core.project_service import ProjectService
from rlgym_learn_api.desc.exception import RLGymLearnApiException
from rlgym_learn_api.desc.project.project import ProjectMetadata
from rlgym_learn_api.desc.project.project_crud_schemas import (
    ProjectCreationArgs,
    ProjectUpdateMetadata,
    ProjectUpdateRoot,
)

router = APIRouter(prefix="/project", tags=["project"])


@router.put("/root", operation_id="update_root_folder")
def update_root(
    args: ProjectUpdateRoot,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    project_service.update_root_folder(args)


@router.get("/root", operation_id="get_root_folder")
def get_root(
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> str:
    return project_service.root_folder


@router.post("", operation_id="create_project")
def create_project(
    args: ProjectCreationArgs,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> str:
    try:
        return project_service.create_project(args)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict(), status_code=e.error_code)


@router.delete("/{project_id}", operation_id="delete_project")
def delete_project(
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    try:
        project_service.delete_project(project_id)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict(), status_code=e.error_code)


@router.put("/{project_id}/meta", operation_id="update_project_metadata")
def update_project_metadata(
    project_id: str,
    project_metadata: ProjectUpdateMetadata,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> None:
    try:
        project_service.update_project_metadata(project_id, project_metadata)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict(), status_code=e.error_code)


@router.get("/all", operation_id="get_all_projects")
def get_all_projects(
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> list[ProjectMetadata]:
    try:
        return project_service.get_all_projects()
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict(), status_code=e.error_code)


@router.get("/{project_id}/meta", operation_id="get_project_metadata")
def get_project_metadata(
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectMetadata:
    try:
        return project_service.get_project_metadata(project_id)
    except RLGymLearnApiException as e:
        return JSONResponse(e.to_dict(), e.error_code)
