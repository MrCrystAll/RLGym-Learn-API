import os
import pathlib
import shutil

from void_api.desc.run import Run
from void_api.infrastructure.run_service import InfrastructureRunService

from pydantic import TypeAdapter


class FSRunService(InfrastructureRunService):
    def create_run(self, path: str, project_id: str, run_name: str):
        _path = pathlib.Path(path) / project_id / "runs"

        _run = Run(project_id=project_id, name=run_name)

        ta = TypeAdapter(list[Run])

        _pyd_runs = ta.validate_json((_path / "runs.json").read_text())

        # Running this before because it checks whether a run with a given name already exists
        os.makedirs(_path / run_name)

        _pyd_runs.append(_run)
        (_path / "runs.json").write_text(ta.dump_json(_pyd_runs).decode())

    def get_runs(self, path: str, project_id: str) -> list[Run]:
        _path = pathlib.Path(path) / project_id / "runs" / "runs.json"

        ta = TypeAdapter(list[Run])

        _pyd_runs = ta.validate_json(_path.read_text())

        return _pyd_runs

    def delete_run(self, path: str, project_id: str, run_name: str):
        _path = pathlib.Path(path) / project_id / "runs"

        ta = TypeAdapter(list[Run])

        _pyd_runs = ta.validate_json((_path / "runs.json").read_text())

        try:
            # Raises ValueError, it means that after this line, we know the run exists in this project
            _pyd_runs.remove(Run(project_id=project_id, name=run_name))
        except ValueError as e:
            raise ValueError(
                f'Run "{run_name}" was not found in the project {project_id}'
            ) from e

        # Raises FileNotFoundError and OSError ?
        shutil.rmtree(_path / run_name, ignore_errors=False)

        (_path / "runs.json").write_text(ta.dump_json(_pyd_runs).decode())
