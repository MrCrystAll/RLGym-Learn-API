import sys
from typing import Any

from requests import ConnectionError, get, post

URL = "http://localhost"


class GUICommunicator:
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

        post(f"{URL}:{self.port}/{self.session_id}/metrics", data=metrics)
