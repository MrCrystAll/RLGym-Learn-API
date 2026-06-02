import os
from datetime import datetime

from rlgym_learn_api.core.project_service import ProjectService
from rlgym_learn_api.core.run_service import RunService
from rlgym_learn_api.desc.project.exceptions import ProjectMalformed
from rlgym_learn_api.desc.run.exceptions import RunConfigMissingError, RunNotFoundError
from rlgym_learn_api.desc.session.exceptions import SessionNotFoundError
from rlgym_learn_api.desc.session.session import LogConfig, Session
from rlgym_learn_api.infrastructure.session_handling import (
    SessionHandler,
    start_entrypoint,
)
from rlgym_learn_api.infrastructure.session_service import InfrastructureSessionService


class SessionService:
    def __init__(
        self,
        project_service: ProjectService,
        run_service: RunService,
        infra_service: InfrastructureSessionService,
    ) -> None:
        self.project_service = project_service
        self.run_service = run_service
        self.infra_service = infra_service

        self.session_handler = SessionHandler()

    def _on_end_session(self, session: Session, return_code: int):
        if return_code == 0:
            session.status = "finished"
        else:
            session.status = "crashed"

        self.session_handler.remove_session(session.session_id)

        try:
            self.infra_service.update_session(self.project_service.root_folder, session)
        except FileNotFoundError:
            # Passing, it means the run has been deleted when the session was running
            pass

    def start_session(self, project_id: str, run_name: str, port: int) -> Session:
        if not self.run_service.run_exists(project_id, run_name):
            raise RunNotFoundError(
                f'Run "{run_name}" doesn\'t exist in project "{project_id}"', run_name
            )

        _sid = str(int(datetime.now().timestamp()))

        _session = Session(
            session_id=_sid,
            status="running",
            project_id=project_id,
            run_name=run_name,
            logs=LogConfig(
                stdout=os.path.join(
                    self.project_service.root_folder,
                    project_id,
                    "runs",
                    run_name,
                    "logs",
                    _sid,
                    "out.log",
                ),
                stderr=os.path.join(
                    self.project_service.root_folder,
                    project_id,
                    "runs",
                    run_name,
                    "logs",
                    _sid,
                    "err.log",
                ),
            ),
        )

        self.infra_service.start_session(self.project_service.root_folder, _session)

        _process = start_entrypoint(
            self.project_service.root_folder,
            self.project_service.get_project_metadata(project_id),
            _session,
            port,
            self._on_end_session,
        )

        self.session_handler.add_session(_sid, _process)

        return _session

    def stop_session(self, session_id: str):
        if not self.session_handler.session_exists(session_id):
            raise SessionNotFoundError(
                session_id, f"Session {session_id} ended or doesn't exist"
            )

        self.session_handler.save_and_stop(session_id)
        return self.session_handler.wait_for_session(session_id)

    def get_all_sessions(self, project_id: str, run_name: str) -> list[Session]:
        try:
            return self.infra_service.get_all_sessions(
                self.project_service.root_folder, project_id, run_name
            )
        except NotADirectoryError as e:
            raise ProjectMalformed(description=str(e), project_id=project_id) from e
        except FileNotFoundError as e:
            raise RunConfigMissingError(description=str(e), run_name=run_name)
        except OSError as e:
            raise RunNotFoundError(description=str(e), run_name=run_name) from e

    def get_session_health(
        self, project_id: str, run_name: str, session_id: str
    ) -> str:
        return self._get_session(project_id, run_name, session_id).status

    def _get_session(self, project_id: str, run_name: str, session_id: str) -> Session:
        try:
            return self.infra_service.get_session(
                self.project_service.root_folder, project_id, run_name, session_id
            )
        except NotADirectoryError as e:
            raise ProjectMalformed(description=str(e), project_id=project_id) from e
        except FileNotFoundError as e:
            raise RunConfigMissingError(description=str(e), run_name=run_name) from e
        except OSError as e:
            raise RunNotFoundError(description=str(e), run_name=run_name) from e
        except ValueError as e:
            raise SessionNotFoundError(session_id=session_id, description=str(e)) from e
