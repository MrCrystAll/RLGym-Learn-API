from rlgym_learn_api.desc.project.exceptions import (
    ProjectCreationFailed,
    ProjectMalformed,
    ProjectNotFoundError,
    ProjectRootFolderNotFound,
)
from rlgym_learn_api.desc.project.project_crud_schemas import (
    ProjectCreationArgs,
    ProjectUpdateMetadata,
    ProjectUpdateRoot,
)
from rlgym_learn_api.infrastructure.project_service import InfrastructureProjectService


class ProjectService:
    def __init__(self, infra_service: InfrastructureProjectService) -> None:
        self.infra_service = infra_service
        self.root_folder = "."

    def update_root_folder(self, args: ProjectUpdateRoot):
        self.root_folder = args.path

    def create_project(self, project_args: ProjectCreationArgs):
        if project_args.interpreter is None:
            project_args.interpreter = "python"

        try:
            return self.infra_service.create_project(self.root_folder, project_args)
        except ValueError as e:
            raise ProjectCreationFailed(
                error_code=417,  # Malformed
                inner_exception=e,
                name=project_args.name,
            ) from e
        except OSError as e:
            raise ProjectCreationFailed(
                error_code=404,  # Not found
                inner_exception=e,
                name=project_args.name,
            ) from e

    def delete_project(self, project_id: str):
        try:
            self.infra_service.delete_project(self.root_folder, project_id)
        except OSError as e:
            raise ProjectNotFoundError(
                project_id=project_id, inner_message=str(e)
            ) from e

    def update_project_metadata(
        self, project_id: str, project_metadata: ProjectUpdateMetadata
    ):
        try:
            self.infra_service.update_project_metadata(
                self.root_folder, project_id, project_metadata
            )
        except OSError as e:
            raise ProjectNotFoundError(
                project_id=project_id, inner_message=str(e)
            ) from e

    def get_all_projects(self):
        try:
            return self.infra_service.get_all_projects(self.root_folder)
        except OSError as e:
            raise ProjectRootFolderNotFound(self.root_folder) from e

    def get_project_metadata(self, project_id: str):
        try:
            return self.infra_service.get_project_metadata(self.root_folder, project_id)
        except OSError as e:
            raise ProjectNotFoundError(
                project_id=project_id, inner_message=str(e)
            ) from e
        except ValueError as e:
            raise ProjectMalformed(project_id=project_id, inner_message=str(e)) from e

    def project_exists(self, project_id: str) -> bool:
        return self.infra_service.project_exists(self.root_folder, project_id)
