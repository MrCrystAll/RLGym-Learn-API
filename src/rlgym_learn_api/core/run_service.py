from typing import Any

from rlgym_learn_algos.ppo.ppo_agent_controller import PPOAgentControllerConfigModel

from rlgym_learn_api.core.project_service import ProjectService
from rlgym_learn_api.desc.project.exceptions import ProjectNotFoundError
from rlgym_learn_api.desc.run.exceptions import (
    RunAlreadyExistsError,
    RunConfigMissingError,
    RunNotFoundError,
    UnknownConfigType,
)
from rlgym_learn_api.infrastructure.run_service import InfrastructureRunService


class RunService:
    def __init__(
        self, project_service: ProjectService, run_service: InfrastructureRunService
    ) -> None:
        self.project_service = project_service
        self.infra_service = run_service

    def _check_project_exists(self, project_id: str):
        if not self.project_service.project_exists(project_id):
            raise ProjectNotFoundError(project_id)

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
            raise RunAlreadyExistsError(run_name) from e

    def delete_run(self, project_id: str, run_name: str):
        self._check_project_exists(project_id)
        try:
            self.infra_service.delete_run(
                self.project_service.root_folder, project_id, run_name
            )
        except ValueError as e:
            raise ProjectNotFoundError(
                project_id=project_id, inner_message=str(e)
            ) from e

    def get_all_runs(self, project_id: str):
        self._check_project_exists(project_id)
        return self.infra_service.get_runs(self.project_service.root_folder, project_id)

    def update_run_data(
        self, project_id: str, run_name: str, raw_config: dict[str, Any]
    ):
        self._check_project_exists(project_id)
        try:
            self.infra_service.update_run_data(
                self.project_service.root_folder, project_id, run_name, raw_config
            )
        except FileNotFoundError as e:
            raise RunConfigMissingError(run_name=run_name) from e

    def get_run_data(self, project_id: str, run_name: str):
        self._check_project_exists(project_id=project_id)
        try:
            return self.infra_service.get_run_data(
                self.project_service.root_folder, project_id, run_name
            )
        except ValueError as e:
            raise RunNotFoundError(run_name=run_name) from e
        except FileNotFoundError as e:
            raise RunConfigMissingError(run_name=run_name) from e

    def _get_ppo_default_config(self, run_name: str):
        return PPOAgentControllerConfigModel(run_name=run_name)

    def get_default_config(self, project_id: str, run_name: str, config_type: str):
        if config_type == "ppo":
            return self._get_ppo_default_config(run_name)
        raise UnknownConfigType(config_type)
