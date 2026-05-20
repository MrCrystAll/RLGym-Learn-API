from void_api.desc.project_crud_schemas import (
    ProjectCreationArgs,
    ProjectUpdateMetadata,
    ProjectUpdateRoot,
)
from void_api.infrastructure.project_service import InfrastructureProjectService


class ProjectService:
    def __init__(self, infra_service: InfrastructureProjectService) -> None:
        self.infra_service = infra_service
        self.root_folder = "."

    def update_root_folder(self, args: ProjectUpdateRoot):
        self.root_folder = args.path

    def create_project(self, project_args: ProjectCreationArgs):
        if project_args.interpreter is None:
            project_args.interpreter = "python"

        return self.infra_service.create_project(self.root_folder, project_args)

    def delete_project(self, project_id: str):
        self.infra_service.delete_project(self.root_folder, project_id)

    def update_project_metadata(
        self, project_id: str, project_metadata: ProjectUpdateMetadata
    ):
        self.infra_service.update_project_metadata(
            self.root_folder, project_id, project_metadata
        )

    def get_all_projects(self):
        return self.infra_service.get_all_projects(self.root_folder)

    def get_project_metadata(self, project_id: str):
        return self.infra_service.get_project_metadata(self.root_folder, project_id)

    def project_exists(self, project_id: str) -> bool:
        return self.infra_service.project_exists(self.root_folder, project_id)
