import os
from os.path import abspath

from rlgym_learn_venv_manager.api.factory import (
    VenvFactoryConfig,
    VirtualEnvironmentFactory,
)
from rlgym_learn_venv_manager.api.virtual_environment import (
    VenvConfig,
    VirtualEnvironment,
)

from rlgym_learn_api.core.project_service import ProjectService
from rlgym_learn_api.desc.project.project_crud_schemas import ProjectUpdateMetadata
from rlgym_learn_api.desc.venv_manager.crud_operations import (
    VenvPreset,
    get_preset_dependencies,
)
from rlgym_learn_api.desc.venv_manager.exceptions import (
    PackageExists,
    ProjectInterpreterNotConfigured,
    VenvCommandFailed,
    VenvCreationFailed,
    VenvDeletionFailed,
    VenvDoesntExist,
)


class VenvManagerService:
    def __init__(self, project_service: ProjectService) -> None:
        self._project_service = project_service

    def create_venv(
        self,
        project_id: str,
        python_executable: str | os.PathLike[str],
        preset: VenvPreset | None,
    ):
        _project_root = os.path.join(self._project_service.root_folder, project_id)

        if not os.path.exists(_project_root):
            raise VenvCreationFailed(
                f'Project "{project_id}" doesn\'t exist at path {abspath(self._project_service.root_folder)}',
                404,
            )

        _venv_factory = VirtualEnvironmentFactory()
        _venv_factory_config = VenvFactoryConfig(
            base_requirements=get_preset_dependencies(preset),
            path_to_project=_project_root,
            python_base_executable=python_executable,
        )
        _venv_factory.load(_venv_factory_config)

        try:
            _venv = _venv_factory.create()
            self._project_service.update_project_metadata(
                project_id=project_id,
                project_metadata=ProjectUpdateMetadata(
                    interpreter=_venv.config.python_executable
                ),
            )
        except ValueError as e:
            raise VenvCreationFailed(description=str(e), error_code=500)
        return _venv.config

    def delete_venv(self, project_id: str):
        _venv = self._load_venv_from_project_id(project_id)

        try:
            _venv.delete()
            self._project_service.update_interpreter(
                project_id=project_id, interpreter=None
            )  # Set to None to show the user that the project now has nothing as the interpreter
        except OSError as e:
            raise VenvDeletionFailed(str(e), 500)

    def _assert_venv_exists(self, python_executable: str | os.PathLike[str]):
        if not os.path.exists(python_executable):
            raise VenvDoesntExist(
                f"Virtual environment not found at path {python_executable}"
            )

    def _load_venv_from_project_id(self, project_id: str) -> VirtualEnvironment:
        _project_metadata = self._project_service.get_project_metadata(project_id)

        if _project_metadata.interpreter is None:
            raise ProjectInterpreterNotConfigured()
        self._assert_venv_exists(_project_metadata.interpreter)

        _venv = VirtualEnvironment()
        _venv_config = VenvConfig(python_executable=_project_metadata.interpreter)
        _venv.load(_venv_config)
        return _venv

    def install(
        self,
        project_id: str,
        package_name: str,
        *extra_args: str,
    ):
        _venv = self._load_venv_from_project_id(project_id)

        if package_name in _venv.pip.list().keys():
            raise PackageExists(f"The package {package_name} already exists.")

        try:
            _venv.install_package(package_name, *extra_args)
        except ValueError as e:
            raise VenvCommandFailed(
                title="Package install failed unexpectedly",
                description=str(e),
                error_code=500,
            )

    def install_requirements(
        self, project_id: str, requirements_path: str | os.PathLike[str], *args
    ):
        _venv = self._load_venv_from_project_id(project_id)

        try:
            _venv.install_requirements(requirements_path, *args)
        except ValueError as e:
            raise VenvCommandFailed(
                title="Error during requirements installation",
                description=str(e),
                error_code=500,
            )

    def get_updatable_packages(self, project_id: str) -> dict[str, str]:
        _venv = self._load_venv_from_project_id(project_id)
        try:
            return _venv.get_all_update_status()
        except ValueError as e:
            raise VenvCommandFailed(
                title="Error during the fetching of updatable packages",
                description=str(e),
                error_code=500,
            )

    def update_package(self, project_id: str, package_name: str):
        _venv = self._load_venv_from_project_id(project_id)
        try:
            _venv.update(package_name)
        except ValueError as e:
            raise VenvCommandFailed(
                title="Error during package update", description=str(e), error_code=500
            )
