import json
import os
import pathlib
import subprocess
import threading
from datetime import datetime
from typing import IO, Callable

from void_api.desc.project import ProjectMetadata
from void_api.desc.session import Session


def start_entrypoint(
    root_folder: str,
    project_metadata: ProjectMetadata,
    session: Session,
    on_end_cb: Callable[[Session, int], None],
):
    _path = pathlib.Path(root_folder) / project_metadata.id / "runs" / session.run_name

    _entrypoint = _path / "src" / "main.py"

    process = subprocess.Popen(
        [project_metadata.interpreter, _entrypoint],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        cwd=str(_path / "src"),
        text=True,
        bufsize=1,  # line-buffered,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},  # if spawning Python subprocesses
    )

    def on_end():
        return_code = process.wait()

        on_end_cb(session, return_code)

    def stream(_stream: IO[str], log_path: str):
        with open(log_path, "w", buffering=1) as f:
            for line in _stream:
                entry = {
                    "timestamp": datetime.now().isoformat(),
                    "line": line.rstrip(),
                    "pid": process.pid,
                }
                f.write(json.dumps(entry) + "\n")
                f.flush()

    threading.Thread(
        target=stream,
        daemon=True,
        args=(process.stdout, os.path.join(root_folder, session.logs.stdout)),
    ).start()
    threading.Thread(
        target=stream,
        daemon=True,
        args=(process.stderr, os.path.join(root_folder, session.logs.stderr)),
    ).start()
    threading.Thread(
        target=on_end,
        daemon=True,
    ).start()

    return process


class SessionHandler:
    def __init__(self) -> None:
        self.sessions: dict[str, subprocess.Popen[str]] = {}

    def add_session(self, session_id: str, process: subprocess.Popen[str]):
        self.sessions[session_id] = process

    def session_exists(self, session_id: str):
        return session_id in self.sessions

    def remove_session(self, session_id: str):
        self.sessions.pop(session_id)

    def wait_for_session(self, session_id: str):
        if not self.session_exists(session_id):
            return -1

        try:
            return self.sessions[session_id].wait(5.0)
        except subprocess.TimeoutExpired:
            self.sessions[session_id].terminate()
            return -1

    def _write_to_stdin(self, session_id: str, data: str):
        if not self.session_exists(session_id):
            return

        _session = self.sessions[session_id]

        if _session.stdin is None:
            raise OSError("The started session has no input descriptor")

        _session.stdin.write(data + "\r\n")
        _session.stdin.flush()

    def save_and_stop(self, session_id: str):
        self._write_to_stdin(session_id, "q")

    def checkpoint(self, session_id: str):
        self._write_to_stdin(session_id, "c")
