from abc import ABC, abstractmethod

from void_api.desc.session import Session


class InfrastructureSessionService(ABC):
    @abstractmethod
    def start_session(self, root_folder: str, session: Session):
        pass

    @abstractmethod
    def update_session(self, root_folder: str, session: Session):
        pass

    @abstractmethod
    def get_session(
        self, root_folder: str, project_id: str, run_name: str, session_id: str
    ) -> Session:
        pass
    
    @abstractmethod
    def get_all_sessions(
        self, root_folder: str, project_id: str, run_name: str
    ) -> list[Session]:
        pass
