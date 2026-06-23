import os
from os.path import abspath

from rlgym_learn_venv_manager.api.factory import (
    VenvFactoryConfig,
    VirtualEnvironmentFactory,
)

from rlgym_learn_api.core.project_service import ProjectService
from rlgym_learn_api.desc.venv_manager.crud_operations import (
    VenvPreset,
    get_preset_dependencies,
)
from rlgym_learn_api.desc.venv_manager.exceptions import VenvCreationFailed


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
        except ValueError as e:
            raise VenvCreationFailed(description=str(e), error_code=500)
        return _venv.config
