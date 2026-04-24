from datetime import datetime
import json
import os
import pathlib
import subprocess
import threading
from typing import IO

from void_api.desc.project import ProjectMetadata
from void_api.infrastructure.filesystem.project_service import PROJECT_CONFIG_JSON_FILE


def start_entrypoint(project_folder: str):
    _path = pathlib.Path(project_folder)

    _pyd_config = ProjectMetadata.model_validate_json(
        (_path / PROJECT_CONFIG_JSON_FILE).read_text()
    )
    _log_path = _path / "logs"
    _entrypoint = _path / "src" / "main.py"

    os.makedirs(_log_path, exist_ok=True)

    process = subprocess.Popen(
        [_pyd_config.interpreter, _entrypoint],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        cwd=os.path.join(_entrypoint, ".."),
        text=True,
        bufsize=1,  # line-buffered,
        env={**os.environ, "PYTHONUNBUFFERED": "1"},  # if spawning Python subprocesses
    )

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

    _out_path = _log_path / "stdout.log"
    _err_path = _log_path / "stderr.log"

    (_path / PROJECT_CONFIG_JSON_FILE).write_text(_pyd_config.model_dump_json())

    threading.Thread(
        target=stream, daemon=True, args=(process.stdout, _out_path)
    ).start()
    threading.Thread(
        target=stream, daemon=True, args=(process.stderr, _err_path)
    ).start()

    return process
