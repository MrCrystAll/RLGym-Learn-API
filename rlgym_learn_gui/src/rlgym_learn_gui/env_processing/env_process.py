import random
import signal
import socket
from dataclasses import dataclass
from multiprocessing import SharedMemory
from typing import Callable, Optional

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
from rlgym_learn.rlgym_learn import PickleablePyAnySerdeType, recvfrom_byte, sendto_byte

try:
    import numpy as np

    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


@dataclass
class PickleableSerdeTypeConfig:
    agent_id_serde_type: PickleablePyAnySerdeType
    action_serde_type: PickleablePyAnySerdeType
    obs_serde_type: PickleablePyAnySerdeType
    reward_serde_type: PickleablePyAnySerdeType
    obs_space_serde_type: PickleablePyAnySerdeType
    action_space_serde_type: PickleablePyAnySerdeType
    shared_info_serde_type: Optional[PickleablePyAnySerdeType]
    shared_info_setter_serde_type: Optional[PickleablePyAnySerdeType]
    state_serde_type: Optional[PickleablePyAnySerdeType]


def env_process(
    proc_id: str,
    parent_sockname,
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
    flinks_folder: str,
    shm_buffer_size: int,
    seed: int,
    render_delay: Optional[float],
):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    child_end = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    child_end.bind(("127.0.0.1", 0))

    random.seed(seed)
    if NUMPY_AVAILABLE:
        np.random.seed(seed)

    sendto_byte(child_end, parent_sockname)
    recvfrom_byte(child_end)

    _shmem = SharedMemory()
