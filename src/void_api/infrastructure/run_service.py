from abc import ABC, abstractmethod

from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel
from void_api.desc.run import Run


class InfrastructureRunService(ABC):
    @abstractmethod
    def create_run(self, path: str, project_id: str, run_name: str):
        pass

    @abstractmethod
    def get_runs(self, path: str, project_id: str) -> list[Run]:
        pass

    @abstractmethod
    def delete_run(self, path: str, project_id: str, run_name: str):
        pass

    @abstractmethod
    def run_exists(self, path: str, project_id: str, run_name: str) -> bool:
        pass

    @abstractmethod
    def get_run_data(
        self, path: str, project_id: str, run_name: str
    ) -> LearningCoordinatorConfigModel:
        pass

    @abstractmethod
    def update_run_data(
        self,
        path: str,
        project_id: str,
        run_name: str,
        project_config: LearningCoordinatorConfigModel,
    ):
        pass
