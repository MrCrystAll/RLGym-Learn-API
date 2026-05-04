import json
import os
import pathlib
import shutil

from pydantic import TypeAdapter
from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel
from void_api.desc.run import Run
from void_api.infrastructure.project_fs import generate_config, generate_entrypoint
from void_api.infrastructure.run_service import InfrastructureRunService


class FSRunService(InfrastructureRunService):
    def _get_src_path(self, path: str, project_id: str, run_name: str):
        return self._get_run_root_path(path, project_id, run_name) / "src"

    def _get_run_root_path(self, path: str, project_id: str, run_name: str):
        return pathlib.Path(path) / project_id / "runs" / run_name

    def _get_config_path(self, path: str, project_id: str):
        return pathlib.Path(path) / project_id / "runs.json"

    def _get_src_and_config_paths(self, path: str, project_id: str, run_name: str):
        return self._get_src_path(path, project_id, run_name), self._get_config_path(
            path, project_id
        )

    def create_run(self, path: str, project_id: str, run_name: str):
        _src_path, _config_path = self._get_src_and_config_paths(
            path, project_id, run_name
        )
        _root_path = self._get_run_root_path(path, project_id, run_name)

        _run = Run(project_id=project_id, name=run_name)

        ta = TypeAdapter(list[Run])

        _pyd_runs = ta.validate_json(_config_path.read_text())

        # Running this before because it checks whether a run with a given name already exists
        os.makedirs(_root_path)
        (_root_path / "sessions.json").write_text(json.dumps([]))

        os.makedirs(_src_path)
        generate_config(_src_path / "config.json")
        generate_entrypoint(_src_path)

        _pyd_runs.append(_run)
        _config_path.write_text(ta.dump_json(_pyd_runs).decode())

    def get_runs(self, path: str, project_id: str) -> list[Run]:
        _config_path = self._get_config_path(path, project_id)

        ta = TypeAdapter(list[Run])

        _pyd_runs = ta.validate_json(_config_path.read_text())

        return _pyd_runs

    def delete_run(self, path: str, project_id: str, run_name: str):
        _config_path = self._get_config_path(path, project_id)

        _root_path = self._get_run_root_path(path, project_id, run_name)

        ta = TypeAdapter(list[Run])

        _pyd_runs = ta.validate_json(_config_path.read_text())

        try:
            # Raises ValueError, it means that after this line, we know the run exists in this project
            _pyd_runs.remove(Run(project_id=project_id, name=run_name))
        except ValueError as e:
            raise ValueError(
                f'Run "{run_name}" was not found in the project {project_id}'
            ) from e

        # Raises FileNotFoundError and OSError ?
        shutil.rmtree(_root_path, ignore_errors=False)

        _config_path.write_text(ta.dump_json(_pyd_runs).decode())

    def run_exists(self, path: str, project_id: str, run_name: str) -> bool:
        _runs = self.get_runs(path, project_id)

        for _run in _runs:
            if _run.name == run_name:
                return True

        return False

    def get_run_data(
        self, path: str, project_id: str, run_name: str
    ) -> LearningCoordinatorConfigModel:
        _path = self._get_run_root_path(path, project_id, run_name)

        if not _path.is_dir():
            raise OSError("The specified run is not a folder")

        if not self.run_exists(path, project_id, run_name):
            raise ValueError(
                f"The run {run_name} doesn't exists in project {project_id}"
            )

        if not (_path / "src" / "config.json").exists():
            raise ValueError(
                "The project doesn't have any configuration, this means it is probably corrupted"
            )

        return LearningCoordinatorConfigModel.model_validate_json(
            (_path / "src" / "config.json").read_text()
        )

    def update_run_data(
        self,
        path: str,
        project_id: str,
        run_name: str,
        project_config: LearningCoordinatorConfigModel,
    ):
        _path = (
            pathlib.Path(self._get_src_path(path, project_id, run_name)) / "config.json"
        )

        assert _path.exists(), "The config does not exist for this project"

        _path.write_text(project_config.model_dump_json())
