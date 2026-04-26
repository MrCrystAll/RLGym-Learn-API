from datetime import datetime
import os

from void_api.core.project_service import ProjectService
from void_api.core.run_service import RunService
from void_api.desc.session import LogConfig, Session
from void_api.infrastructure.session_handling import SessionHandler, start_entrypoint
from void_api.infrastructure.session_service import InfrastructureSessionService


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

    def start_session(self, project_id: str, run_name: str) -> Session:
        if not self.run_service.run_exists(project_id, run_name):
            raise ValueError(
                f'Run "{run_name}" doesn\'t exist in project "{project_id}"'
            )

        _sid = str(int(datetime.now().timestamp()))

        _session = Session(
            session_id=_sid,
            status="running",
            project_id=project_id,
            run_name=run_name,
            logs=LogConfig(
                stdout=os.path.join(project_id, "logs", _sid, "out.log"),
                stderr=os.path.join(project_id, "logs", _sid, "err.log"),
            ),
        )

        self.infra_service.start_session(self.project_service.root_folder, _session)

        _process = start_entrypoint(
            self.project_service.root_folder,
            self.project_service.get_project_metadata(project_id),
            _session,
            self._on_end_session
        )

        self.session_handler.add_session(_sid, _process)

        return _session

    def stop_session(self, session_id: str):
        if not self.session_handler.session_exists(session_id):
            raise ValueError(f"Session {session_id} ended or doesn't exist")

        self.session_handler.save_and_stop(session_id)
        self.session_handler.wait_for_session(session_id)

    def get_all_sessions(self, project_id: str, run_name: str) -> list[Session]:
        return self.infra_service.get_all_sessions(self.project_service.root_folder, project_id, run_name)