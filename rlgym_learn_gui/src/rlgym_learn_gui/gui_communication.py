import sys
from typing import Any, Generic

import numpy as np
from requests import ConnectionError, get, post
from rlgym.api import ActionSpaceType, ObsSpaceType

URL = "http://localhost"


class GUICommunicator(Generic[ObsSpaceType, ActionSpaceType]):
    def __init__(self, session_id: str, port: int, name: str) -> None:
        self.name = name
        self.port = port
        self.session_id = session_id

    def is_gui_alive(self) -> bool:
        try:
            _response = get(f"{URL}:{self.port}/")
        except ConnectionError:
            return False

        return _response.ok

    def send_metrics(self, metrics: dict[str, Any]):
        if not self.is_gui_alive():
            print("GUI couldn't be found, ignoring", file=sys.stderr)
            return

        for k in metrics.keys():
            if isinstance(metrics[k], np.floating):
                metrics[k] = float(metrics[k])

        post(
            f"{URL}:{self.port}/sessions/{self.session_id}/metrics",
            json=metrics,
        )

    def set_spaces_types(
        self,
        agent_controller_name: str,
        obs_space: ObsSpaceType,
        act_space: ActionSpaceType,
    ):
        if not self.is_gui_alive():
            print("GUI couldn't be found, ignoring", file=sys.stderr)
            return

        post(
            f"{URL}:{self.port}/sessions/{self.session_id}/spaces",
            json={
                "agent_controller_name": agent_controller_name,
                "obs_space": obs_space,
                "act_space": act_space,
            },
        )
