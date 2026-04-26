from void_api.core.project_service import ProjectService
from void_api.core.run_service import RunService
from void_api.core.session_service import SessionService
from void_api.infrastructure.filesystem.project_service import FSProjectService
from void_api.infrastructure.filesystem.run_service import FSRunService
from void_api.infrastructure.filesystem.session_service import FSSessionService


_fs_project_service = FSProjectService()
_fs_run_service = FSRunService()
_fs_session_service = FSSessionService()

_project_service = ProjectService(_fs_project_service)
_run_service = RunService(_project_service, _fs_run_service)
_session_service = SessionService(_project_service, _run_service, _fs_session_service)


def get_project_service() -> ProjectService:
    return _project_service


def get_run_service() -> RunService:
    return _run_service


def get_session_service() -> SessionService:
    return _session_service
