import multiprocessing as mp
import socket
import time
from typing import Callable, Generic, Optional
from uuid import uuid4

from rlgym.api import (
    ActionSpaceType,
    ActionType,
    AgentID,
    EngineActionType,
    ObsSpaceType,
    ObsType,
    RewardType,
    RLGym,
    StateType,
)
from rlgym_learn.api.typing import ActionAssociatedLearningData
from rlgym_learn.learning_coordinator_config import SerdeTypesModel
from rlgym_learn.rlgym_learn import PickleablePyAnySerdeType, recvfrom_byte, sendto_byte

from rlgym_learn_gui.env_processing.env_process import (
    PickleableSerdeTypeConfig,
    env_process,
)

try:
    from tqdm import tqdm
except ImportError:

    def tqdm(iterator, *args, **kwargs):
        return iterator


class EnvProcessInterface(
    Generic[
        AgentID,
        ObsType,
        ActionType,
        EngineActionType,
        RewardType,
        StateType,
        ObsSpaceType,
        ActionSpaceType,
        ActionAssociatedLearningData,
    ]
):
    def __init__(
        self,
        build_env_fn: Callable[
            [],
            RLGym[
                AgentID,
                ObsType,
                ActionType,
                EngineActionType,
                RewardType,
                StateType,
                ObsSpaceType,
                ActionSpaceType,
            ],
        ],
        serde_types: SerdeTypesModel,
        min_process_steps_per_inference: int,
        flinks_folder: str,
        shm_buffer_size: int,
        seed: int,
        recalculate_agent_id_every_step: bool,
    ):
        self.build_env_fn = build_env_fn
        self.serde_type_config = PickleableSerdeTypeConfig(
            PickleablePyAnySerdeType(serde_types.agent_id_serde_type),
            PickleablePyAnySerdeType(serde_types.action_serde_type),
            PickleablePyAnySerdeType(serde_types.obs_serde_type),
            PickleablePyAnySerdeType(serde_types.reward_serde_type),
            PickleablePyAnySerdeType(serde_types.obs_space_serde_type),
            PickleablePyAnySerdeType(serde_types.action_space_serde_type),
            PickleablePyAnySerdeType(serde_types.shared_info_serde_type),
            PickleablePyAnySerdeType(serde_types.shared_info_setter_serde_type),
            PickleablePyAnySerdeType(serde_types.state_serde_type),
        )
        self.n_procs = 0
        self.flinks_folder = flinks_folder
        self.shm_buffer_size = shm_buffer_size

    def init_processes(
        self,
        n_processes: int,
        spawn_delay=None,
        render=False,
        render_delay: Optional[float] = None,
    ):
        can_fork = "forkserver" in mp.get_all_start_methods()
        start_method = "forkserver" if can_fork else "spawn"
        context = mp.get_context(start_method)
        self.n_procs = n_processes

        self.processes = [None for i in range(n_processes)]

        # Spawn child processes
        print("Spawning processes...")
        for proc_idx in tqdm(range(n_processes)):
            proc_id = str(uuid4())

            # Create socket to communicate with child
            parent_end = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            parent_end.bind(("127.0.0.1", 0))

            process = context.Process(
                target=env_process,
                args=(
                    proc_id,
                    parent_end.getsockname(),
                    self.build_env_fn,
                    self.serde_type_config,
                    self.flinks_folder,
                    self.shm_buffer_size,
                ),
                daemon=True,
            )
            process.start()

            self.processes[proc_idx] = (process, parent_end, None, proc_id)

        # Initialize child processes
        print("Initializing processes...")
        for pid_idx in tqdm(range(n_processes)):
            process, parent_end, _, proc_id = self.processes[pid_idx]

            # Get child endpoint
            _, child_sockname = recvfrom_byte(parent_end)
            sendto_byte(parent_end, child_sockname)

            if spawn_delay is not None:
                time.sleep(spawn_delay)

            self.processes[pid_idx] = (
                process,
                parent_end,
                child_sockname,
                proc_id,
            )
