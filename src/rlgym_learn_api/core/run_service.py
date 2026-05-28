from typing import Any

from rlgym_learn_algos.ppo.ppo_agent_controller import PPOAgentControllerConfigModel

from rlgym_learn_api.core.project_service import ProjectService
from rlgym_learn_api.infrastructure.run_service import InfrastructureRunService


class RunService:
    def __init__(
        self, project_service: ProjectService, run_service: InfrastructureRunService
    ) -> None:
        self.project_service = project_service
        self.infra_service = run_service

    def _check_project_exists(self, project_id: str):
        if not self.project_service.project_exists(project_id):
            raise ValueError(f"Project {project_id} doesn't exist")

    def run_exists(self, project_id: str, run_name: str) -> bool:
        self._check_project_exists(project_id)

        return self.infra_service.run_exists(
            self.project_service.root_folder, project_id, run_name
        )

    def create_run(self, project_id: str, run_name: str):
        self._check_project_exists(project_id)

        try:
            self.infra_service.create_run(
                self.project_service.root_folder, project_id, run_name
            )
        except FileExistsError as e:
            raise FileExistsError(
                f'A run with the name "{run_name}" already exists in the project {project_id}'
            ) from e

    def delete_run(self, project_id: str, run_name: str):
        self._check_project_exists(project_id)

        self.infra_service.delete_run(
            self.project_service.root_folder, project_id, run_name
        )

    def get_all_runs(self, project_id: str):
        self._check_project_exists(project_id)

        return self.infra_service.get_runs(self.project_service.root_folder, project_id)

    def update_run_data(
        self, project_id: str, run_name: str, raw_config: dict[str, Any]
    ):
        self.infra_service.update_run_data(
            self.project_service.root_folder, project_id, run_name, raw_config
        )

    def get_run_data(self, project_id: str, run_name: str):
        return self.infra_service.get_run_data(
            self.project_service.root_folder, project_id, run_name
        )

    def _get_ppo_default_config(self, run_name: str):
        return PPOAgentControllerConfigModel(run_name=run_name)

    def get_default_config(self, project_id: str, run_name: str, config_type: str):
        if config_type == "ppo":
            return self._get_ppo_default_config(run_name)
        raise ValueError(f"Unknown default config: {config_type}")
