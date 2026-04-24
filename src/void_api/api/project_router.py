from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response

from void_api.api.services import get_project_service
from void_api.core.project_service import ProjectService
from void_api.desc.project_crud_schemas import (
    ProjectCreationArgs,
    ProjectUpdateMetadata,
    ProjectUpdateRoot,
)

from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel

from void_api.desc.project import ProjectMetadata

router = APIRouter(prefix="/project", tags=["project"])


@router.put("/root", operation_id="update_root_folder")
def update_root(
    args: ProjectUpdateRoot,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    project_service.update_root_folder(args)


@router.get("/root", operation_id="get_root_folder")
def get_root(project_service: Annotated[ProjectService, Depends(get_project_service)]):
    return project_service.root_folder


@router.post("/", operation_id="create_project")
def create_project(
    args: ProjectCreationArgs,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        return project_service.create_project(args)
    except ValueError as e:
        return Response(str(e), status_code=417)


@router.delete("/{project_id}", operation_id="delete_project")
def delete_project(
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        project_service.delete_project(project_id)
    except OSError as e:
        return Response(str(e), status_code=404)


@router.put("/{project_id}/meta", operation_id="update_project_metadata")
def update_project_metadata(
    project_id: str,
    project_metadata: ProjectUpdateMetadata,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    project_service.update_project_metadata(project_id, project_metadata)


@router.put("/{project_id}/config", operation_id="update_project_config")
async def update_project_config(
    project_id: str,
    request: Request,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    raw = await request.body()
    config = LearningCoordinatorConfigModel.model_validate_json(raw)

    project_service.update_project_config(project_id, config)


@router.get("/all", operation_id="get_all_projects")
def get_all_projects(
    project_service: Annotated[ProjectService, Depends(get_project_service)],
) -> list[ProjectMetadata]:
    return project_service.get_all_projects()


@router.get("/{project_id}/data", operation_id="get_project_data")
def get_project_data(
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        return project_service.get_project_data(project_id)
    except OSError as e:
        return Response(content=str(e), status_code=404)
    except ValueError as e:
        return Response(content=str(e), status_code=417)


@router.get("/{project_id}/meta", operation_id="get_project_metadata")
def get_project_metadata(
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        return project_service.get_project_metadata(project_id)
    except OSError as e:
        return Response(content=str(e), status_code=404)
    except ValueError as e:
        return Response(content=str(e), status_code=417)
