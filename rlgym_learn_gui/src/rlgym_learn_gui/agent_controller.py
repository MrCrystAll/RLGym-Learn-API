from typing import Any, Dict, Generic, Iterable, List, Optional, Tuple

from pydantic import BaseModel
from rlgym.api import (
    ActionSpaceType,
    ActionType,
    AgentID,
    ObsSpaceType,
    ObsType,
    RewardType,
    StateType,
)
from rlgym_learn.api.agent_controller import (
    AgentController,
    DerivedAgentControllerConfig,
)
from rlgym_learn.api.typing import (
    ActionAssociatedLearningData,
    AgentControllerConfig,
    AgentControllerData,
)
from rlgym_learn.rlgym_learn import EnvActionResponse, Timestep

from rlgym_learn_gui.gui_communication import GUICommunicator


class GUIAgentControllerConfig(BaseModel, Generic[AgentControllerConfig]):
    inner_agent_controller_config: AgentControllerConfig

    session_id: str
    port: int


class GUIAgentController(
    AgentController[
        GUIAgentControllerConfig[AgentControllerConfig],
        AgentID,
        ObsType,
        ActionType,
        RewardType,
        StateType,
        ObsSpaceType,
        ActionSpaceType,
        ActionAssociatedLearningData,
        AgentControllerData,
    ],
    Generic[
        AgentControllerConfig,
        AgentID,
        ObsType,
        ActionType,
        RewardType,
        StateType,
        ObsSpaceType,
        ActionSpaceType,
        ActionAssociatedLearningData,
        AgentControllerData,
    ],
):
    def __init__(
        self,
        inner_agent_controller: AgentController[
            AgentControllerConfig,
            AgentID,
            ObsType,
            ActionType,
            RewardType,
            StateType,
            ObsSpaceType,
            ActionSpaceType,
            ActionAssociatedLearningData,
            AgentControllerData,
        ],
    ):
        self.inner_agent_controller = inner_agent_controller

    def validate_config(
        self, config_obj: Dict[str, Any]
    ) -> GUIAgentControllerConfig[AgentControllerConfig]:
        _gui_config = GUIAgentControllerConfig.model_validate(config_obj)

        _gui_config.inner_agent_controller_config = (
            self.inner_agent_controller.validate_config(
                config_obj["inner_agent_controller_config"]
            )
        )

        return _gui_config

    def get_actions(
        self, agent_id_list: List[AgentID], obs_list: List[ObsType]
    ) -> Tuple[Iterable[ActionType], ActionAssociatedLearningData]:
        return self.inner_agent_controller.get_actions(agent_id_list, obs_list)

    def choose_agents(self, agent_id_list: List[AgentID]) -> List[int]:
        return self.inner_agent_controller.choose_agents(agent_id_list)

    def choose_env_actions(
        self,
        state_info: Dict[
            str,
            Tuple[
                Optional[Dict[str, Any]],
                Optional[StateType],
                Optional[Dict[AgentID, bool]],
                Optional[Dict[AgentID, bool]],
            ],
        ],
    ) -> Dict[str, Optional[EnvActionResponse]]:
        return self.inner_agent_controller.choose_env_actions(state_info)

    def set_space_types(self, obs_space: ObsSpaceType, action_space: ActionSpaceType):
        self.obs_space = obs_space
        self.action_space = action_space
        self.inner_agent_controller.set_space_types(obs_space, action_space)

    def process_timestep_data(
        self,
        timestep_data: Dict[
            str,
            Tuple[
                List[Timestep],
                Optional[ActionAssociatedLearningData],
                Optional[Dict[str, Any]],
                Optional[StateType],
            ],
        ],
    ):
        self.inner_agent_controller.process_timestep_data(timestep_data)

    def process_env_actions(self, env_actions: Dict[str, EnvActionResponse]):
        self.inner_agent_controller.process_env_actions(env_actions)

    def load(
        self,
        config: DerivedAgentControllerConfig[
            GUIAgentControllerConfig[AgentControllerConfig]
        ],
    ):
        self.config = config

        self.gui_communicator = GUICommunicator(
            config.agent_controller_config.session_id,
            config.agent_controller_config.port,
            "agent_controller",
        )

        # Doing this here because set_space_types is called before load (for obvious reasons that some components need it)
        self.gui_communicator.set_spaces_types(
            self.config.agent_controller_name, self.obs_space, self.action_space
        )

        self.inner_agent_controller.load(
            DerivedAgentControllerConfig(
                agent_controller_config=config.agent_controller_config.inner_agent_controller_config,
                agent_controller_name=config.agent_controller_name,
                base_config=config.base_config,
                process_config=config.process_config,
                save_folder=config.save_folder,
            )
        )

    def save_checkpoint(self):
        self.inner_agent_controller.save_checkpoint()

    def cleanup(self):
        self.inner_agent_controller.cleanup()
