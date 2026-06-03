import os
import pathlib

from pydantic import TypeAdapter

from rlgym_learn_api.desc.session.session import Session
from rlgym_learn_api.infrastructure.session_service import InfrastructureSessionService


class FSSessionService(InfrastructureSessionService):
    def start_session(self, root_folder: str, session: Session):
        _path = pathlib.Path(root_folder)

        # Create log structure
        os.makedirs(pathlib.Path(session.logs.stdout).parent)

        pathlib.Path(session.logs.stdout).touch()
        pathlib.Path(session.logs.stderr).touch()

        _session_path = (
            _path / session.project_id / "runs" / session.run_name / "sessions.json"
        )

        ta = TypeAdapter(list[Session])
        _pyd_sessions = ta.validate_json(_session_path.read_text())

        _pyd_sessions.append(session)

        _session_path.write_bytes(ta.dump_json(_pyd_sessions))

    def update_session(self, root_folder: str, session: Session):
        _path = (
            pathlib.Path(root_folder) / session.project_id / "runs" / session.run_name
        )

        ta = TypeAdapter(list[Session])

        _pyd_sessions = ta.validate_json((_path / "sessions.json").read_text())

        _idx = 0

        for i in range(len(_pyd_sessions)):
            if _pyd_sessions[i] == session:
                _idx = i
                break

        _pyd_sessions[_idx] = session

        (_path / "sessions.json").write_bytes(ta.dump_json(_pyd_sessions))

    def get_session(
        self, root_folder: str, project_id: str, run_name: str, session_id: str
    ) -> Session:
        _pyd_sessions = self.get_all_sessions(root_folder, project_id, run_name)

        for _session in _pyd_sessions:
            if _session.session_id == session_id:
                return _session

        raise ValueError(
            f"Session {session_id} not found in run {run_name} of project {project_id}"
        )

    def get_all_sessions(
        self, root_folder: str, project_id: str, run_name: str
    ) -> list[Session]:
        _path = pathlib.Path(root_folder) / project_id / "runs" / run_name

        if not _path.exists():
            raise OSError(f"The path {_path.absolute()} doesn't exist")

        if not _path.is_dir():
            raise NotADirectoryError(f"The path {_path.absolute()} is not a directory")

        if not (_path / "sessions.json").exists():
            raise FileNotFoundError(
                f"The sessions.json file doesn't exist in the run {run_name} folder"
            )

        ta = TypeAdapter(list[Session])
        _pyd_sessions = ta.validate_json((_path / "sessions.json").read_text())

        return _pyd_sessions
