import json
import os
import pathlib
import shutil
import uuid

from pydantic import ValidationError

from rlgym_learn_api.desc.project.project import ProjectMetadata
from rlgym_learn_api.desc.project.project_crud_schemas import (
    ProjectCreationArgs,
    ProjectUpdateMetadata,
)
from rlgym_learn_api.infrastructure.project_fs import generate_project_directory
from rlgym_learn_api.infrastructure.project_service import InfrastructureProjectService

PROJECT_CONFIG_JSON_FILE = "project_config.json"


class FSProjectService(InfrastructureProjectService):
    def create_project(self, path: str, project_args: ProjectCreationArgs) -> str:

        if project_args.interpreter is None:
            raise ValueError("Validation failed for project creation")
        if not os.path.exists(path):
            raise OSError(f"Folder path {path} doesn't exist")

        _id = str(uuid.uuid4())

        _folder_path = pathlib.Path(os.path.join(path, _id))
        os.makedirs(_folder_path)

        (_folder_path / PROJECT_CONFIG_JSON_FILE).write_text(
            ProjectMetadata(
                name=project_args.name, id=_id, interpreter=project_args.interpreter
            ).model_dump_json()
        )

        (_folder_path / "runs.json").write_text(json.dumps([]))

        generate_project_directory(str(_folder_path))

        return _id

    def update_project_metadata(
        self, path: str, project_id: str, metadata: ProjectUpdateMetadata
    ):
        _path = pathlib.Path(os.path.join(path, project_id))
        if not os.path.exists(_path):
            raise OSError("The specified project doesn't exist")

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

    def get_all_projects(self, path: str) -> list[ProjectMetadata]:
        _projects = []

        if not os.path.exists(path):
            raise OSError(f'Folder path "{path}" doesn\'t exist')

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
