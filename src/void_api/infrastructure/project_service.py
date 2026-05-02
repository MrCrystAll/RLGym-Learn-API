from abc import ABC, abstractmethod

from void_api.desc.project import ProjectMetadata
from void_api.desc.project_crud_schemas import (
    ProjectCreationArgs,
    ProjectUpdateMetadata,
)


class InfrastructureProjectService(ABC):
    @abstractmethod
    def create_project(self, path: str, project_args: ProjectCreationArgs) -> str:
        pass

    @abstractmethod
    def delete_project(self, path: str, project_id: str):
        pass

    @abstractmethod
    def update_project_metadata(
        self, path: str, project_id: str, metadata: ProjectUpdateMetadata
    ):
        pass

    @abstractmethod
    def get_all_projects(self, path: str) -> list[ProjectMetadata]:
        pass

    @abstractmethod
    def get_project_metadata(self, path: str, project_id: str) -> ProjectMetadata:
        pass

    @abstractmethod
    def project_exists(self, path: str, project_id: str) -> bool:
        pass
