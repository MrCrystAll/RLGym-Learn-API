from abc import ABC, abstractmethod
from typing import Any

from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel

from rlgym_learn_api.desc.run.run import Run


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
    def get_run_data(self, path: str, project_id: str, run_name: str) -> dict[str, Any]:
        pass

    @abstractmethod
    def update_run_data(
        self,
        path: str,
        project_id: str,
        run_name: str,
        config: LearningCoordinatorConfigModel,
    ):
        pass
