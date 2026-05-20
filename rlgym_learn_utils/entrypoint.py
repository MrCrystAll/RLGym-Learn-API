# Main entrypoint of a run

import json
import os
import pathlib
import sys
import traceback

# needed to prevent numpy from using a ton of memory in env processes and causing them to throttle each other
os.environ["OPENBLAS_NUM_THREADS"] = "1"


# You can modify this function without any issue
def build_rlgym_v2_env():
    import numpy as np
    from rlgym.api import RLGym
    from rlgym.rocket_league import common_values
    from rlgym.rocket_league.action_parsers import LookupTableAction, RepeatAction
    from rlgym.rocket_league.done_conditions import (
        AnyCondition,
        GoalCondition,
        NoTouchTimeoutCondition,
        TimeoutCondition,
    )
    from rlgym.rocket_league.obs_builders import DefaultObs
    from rlgym.rocket_league.reward_functions import (
        CombinedReward,
        GoalReward,
        TouchReward,
    )
    from rlgym.rocket_league.sim import RocketSimEngine
    from rlgym.rocket_league.state_mutators import (
        FixedTeamSizeMutator,
        KickoffMutator,
        MutatorSequence,
    )

    spawn_opponents = True
    team_size = 2
    blue_team_size = team_size
    orange_team_size = team_size if spawn_opponents else 0
    action_repeat = 8
    no_touch_timeout_seconds = 30
    game_timeout_seconds = 300

    action_parser = RepeatAction(LookupTableAction(), repeats=action_repeat)
    termination_condition = GoalCondition()
    truncation_condition = AnyCondition(
        NoTouchTimeoutCondition(timeout_seconds=no_touch_timeout_seconds),
        TimeoutCondition(timeout_seconds=game_timeout_seconds),
    )

    reward_fn = CombinedReward((GoalReward(), 10), (TouchReward(), 0.1))

    obs_builder = DefaultObs(
        zero_padding=team_size,
        pos_coef=np.asarray(
            [
                1 / common_values.SIDE_WALL_X,
                1 / common_values.BACK_NET_Y,
                1 / common_values.CEILING_Z,
            ]
        ),
        ang_coef=1 / np.pi,
        lin_vel_coef=1 / common_values.CAR_MAX_SPEED,
        ang_vel_coef=1 / common_values.CAR_MAX_ANG_VEL,
        boost_coef=1 / 100.0,
    )

    state_mutator = MutatorSequence(
        FixedTeamSizeMutator(blue_size=blue_team_size, orange_size=orange_team_size),
        KickoffMutator(),
    )
    return RLGym(
        state_mutator=state_mutator,
        obs_builder=obs_builder,
        action_parser=action_parser,
        reward_fn=reward_fn,
        termination_cond=termination_condition,
        truncation_cond=truncation_condition,
        transition_engine=RocketSimEngine(),
    )


if __name__ == "__main__":
    # I HIGHLY DISCOURAGE you to modify this part as it may cause unexpected crashes / unplanned stuff
    # Modify at your own risk
    #
    from argparse import ArgumentParser
    from typing import Tuple

    parser = ArgumentParser()
    parser.add_argument("--session", help="The ID of the session")
    parser.add_argument("--run", help="The run of the session")
    parser.add_argument("--project", help="The project of the run")
    args = parser.parse_args()

    from rlgym_learn import (
        LearningCoordinator,
    )
    from rlgym_learn.learning_coordinator_config import LearningCoordinatorConfigModel
    from rlgym_learn_algos.ppo import (
        BasicCritic,
        DiscreteFF,
        GAETrajectoryProcessor,
        NumpyExperienceBuffer,
        PPOAgentController,
        PPOMetricsLogger,
    )

    # from rlgym_learn_algos.util.checkpoint_saving.checkpoint_handler import (
    #     CheckpointHandler,
    # )
    # from rlgym_learn_algos.util.checkpoint_saving.loading_strategy import (
    #     LoadLatestCheckpoint,
    # )
    # from rlgym_learn_algos.util.checkpoint_saving.saving_strategy import (
    #     KeepLastCheckpoints,
    #     SaveTimestamps,
    # )
    from rlgym_learn_gui.agent_controller import (
        GUIAgentController,
        GUIAgentControllerConfig,
    )
    from rlgym_learn_gui.metrics_logger import GUIMetricsLogger, GUIMetricsLoggerConfig

    # The obs_space_type and action_space_type are determined by your choice of ObsBuilder and ActionParser respectively.
    # The logic used here assumes you are using the types defined by the DefaultObs and LookupTableAction above.
    DefaultObsSpaceType = Tuple[str, int]
    DefaultActionSpaceType = Tuple[str, int]

    def actor_factory(
        obs_space: DefaultObsSpaceType,
        action_space: DefaultActionSpaceType,
        device: str,
    ):
        return DiscreteFF(obs_space[1], action_space[1], (256, 256, 256), device)

    def critic_factory(obs_space: DefaultObsSpaceType, device: str):
        return BasicCritic(obs_space[1], (256, 256, 256), device)

    try:
        _json_config = json.loads(pathlib.Path("config.json").read_text())
        _json_agent_controllers_config = _json_config["agent_controllers_config"]

        _gui_metrics_logger_config = GUIMetricsLoggerConfig(
            project_id=args.project,
            run_name=args.run,
            port=8000,
            inner_metrics_logger_config=None,
        )
        _gui_agent_controller_config = GUIAgentControllerConfig(
            session_id=args.session, port=8000, inner_agent_controller_config=None
        )

        agent_controllers = {
            agent: GUIAgentController(
                PPOAgentController(
                    actor_factory=actor_factory,
                    critic_factory=critic_factory,
                    experience_buffer=NumpyExperienceBuffer(GAETrajectoryProcessor()),
                    metrics_logger=GUIMetricsLogger(PPOMetricsLogger()),
                    # checkpoint_handler=CheckpointHandler(
                    #     load_strategy=LoadLatestCheckpoint(),
                    #     save_strategy=KeepLastCheckpoints(SaveTimestamps()),
                    # ),
                    obs_standardizer=None,
                )
            )
            for agent in _json_agent_controllers_config.keys()
        }

        for _agent_controller_id in _json_agent_controllers_config.keys():
            try:
                _gui_agent_controller_config.inner_agent_controller_config = (
                    _json_config["agent_controllers_config"][_agent_controller_id]
                )

                _gui_metrics_logger_config.inner_metrics_logger_config = _json_config[
                    "agent_controllers_config"
                ][_agent_controller_id]["metrics_logger_config"]
            except AttributeError:
                pass
            finally:
                _json_config["agent_controllers_config"][_agent_controller_id] = (
                    _gui_agent_controller_config.model_dump()
                )

                _json_config["agent_controllers_config"][_agent_controller_id][
                    "inner_agent_controller_config"
                ]["metrics_logger_config"] = _gui_metrics_logger_config.model_dump()

        _config = LearningCoordinatorConfigModel.model_validate_json(
            json.dumps(_json_config), context=agent_controllers
        )

        learning_coordinator = LearningCoordinator(
            build_rlgym_v2_env,
            agent_controllers=agent_controllers,
            config=_config,
        )

        learning_coordinator.start()
        print("Process finished.")
    except Exception as e:
        _lines = traceback.format_exception(e)
        for _line in _lines:
            print(_line, file=sys.stderr, flush=True)
        sys.exit(1)
