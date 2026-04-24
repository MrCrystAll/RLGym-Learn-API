import os
import pathlib
import shutil
import uuid

from pydantic import ValidationError

from void_api.desc.project_crud_schemas import (
    ProjectCreationArgs,
    ProjectUpdateMetadata,
)
from void_api.desc.project import ProjectMetadata
from void_api.infrastructure.project_fs import generate_project_directory
from void_api.infrastructure.project_service import InfrastructureProjectService

from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel

PROJECT_CONFIG_JSON_FILE = "project_config.json"


class FSProjectService(InfrastructureProjectService):
    def create_project(self, path: str, project_args: ProjectCreationArgs) -> str:

        if project_args.interpreter is None:
            raise ValueError("Validation failed for project creation")

        _id = str(uuid.uuid4())

        _folder_path = pathlib.Path(os.path.join(path, _id))
        os.makedirs(_folder_path)

        (_folder_path / PROJECT_CONFIG_JSON_FILE).write_text(
            ProjectMetadata(
                name=project_args.name, id=_id, interpreter=project_args.interpreter
            ).model_dump_json()
        )

        generate_project_directory(str(_folder_path))

        return _id

    def update_project_metadata(
        self, path: str, project_id: str, metadata: ProjectUpdateMetadata
    ):
        _path = pathlib.Path(os.path.join(path, project_id))
        assert os.path.exists(_path), f"Cannot access folder {_path}"

        _pyd_config = ProjectMetadata.model_validate_json(
            (_path / PROJECT_CONFIG_JSON_FILE).read_text()
        )

        if metadata.name is not None:
            _pyd_config.name = metadata.name
        if metadata.interpreter is not None:
            _pyd_config.interpreter = metadata.interpreter

        (_path / PROJECT_CONFIG_JSON_FILE).write_text(_pyd_config.model_dump_json())

    def delete_project(self, path: str, project_id: str):
        _path = pathlib.Path(os.path.join(path, project_id))

        if not _path.exists():
            raise OSError(
                f"The project '{project_id}' doesn't exist in the folder {_path.parent.absolute()}"
            )

        shutil.rmtree(os.path.join(path, project_id))

    def update_project_config(
        self, path: str, project_id: str, project_config: LearningCoordinatorConfigModel
    ):
        _path = pathlib.Path(os.path.join(path, project_id)) / "src" / "config.json"

        assert _path.exists(), "The config does not exist for this project"

        _path.write_text(project_config.model_dump_json())

    def get_all_projects(self, path: str) -> list[ProjectMetadata]:
        _projects = []

        for _dir in os.listdir(path):
            _path = pathlib.Path(path) / _dir

            if not _path.is_dir():
                continue

            if not (_path / PROJECT_CONFIG_JSON_FILE).exists():
                continue

            try:
                _config_file = _path / PROJECT_CONFIG_JSON_FILE
                _projects.append(
                    ProjectMetadata.model_validate_json(_config_file.read_text())
                )
            except ValidationError:
                pass

        return _projects

    def get_project_data(
        self, path: str, project_id: str
    ) -> LearningCoordinatorConfigModel:
        _path = pathlib.Path(path) / project_id

        if not _path.exists():
            raise OSError("The specified project doesn't exist")

        if not _path.is_dir():
            raise OSError("The specified project is not a folder")

        if not (_path / PROJECT_CONFIG_JSON_FILE).exists():
            raise ValueError(
                "The specified project is not a rlgym-learn-gui project and cannot be opened"
            )

        if not (_path / "src" / "config.json").exists():
            raise ValueError(
                "The project doesn't have any configuration, this means it is probably corrupted"
            )

        return LearningCoordinatorConfigModel.model_validate_json(
            (_path / "src" / "config.json").read_text()
        )

    def get_project_metadata(self, path: str, project_id: str) -> ProjectMetadata:
        _path = pathlib.Path(path) / project_id

        if not _path.exists():
            raise OSError("The specified project doesn't exist")

        if not _path.is_dir():
            raise OSError("The specified project is not a folder")

        if not (_path / PROJECT_CONFIG_JSON_FILE).exists():
            raise ValueError(
                "The specified project is not a rlgym-learn-gui project and cannot be opened"
            )

        return ProjectMetadata.model_validate_json(
            (_path / PROJECT_CONFIG_JSON_FILE).read_text()
        )

    def project_exists(self, path: str, project_id: str) -> bool:
        _path = pathlib.Path(path) / project_id

        return (
            _path.exists()
            and _path.is_dir()
            and (_path / PROJECT_CONFIG_JSON_FILE).exists()
        )
