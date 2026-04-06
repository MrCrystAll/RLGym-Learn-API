from datetime import datetime
import json
import os
import pathlib
import subprocess

from void_api.common_values import PROJECT_CONFIG_JSON_FILE
from void_api.primitives import Project, ProjectMetadata


def start_entrypoint(python_path: str, project_metadata: ProjectMetadata):
    assert project_metadata.path is not None, "Can't start entrypoint if no path"
    
    _path = pathlib.Path(project_metadata.path)
    
    _pyd_config = Project.model_validate_json(
        (_path / PROJECT_CONFIG_JSON_FILE).read_text()
    )
    _log_path = _path / _pyd_config.data.log_config.stdout_log
    
    os.makedirs(_log_path.parent, exist_ok=True)
    
    assert _pyd_config.data.entrypoint is not None, "No entrypoint found"
    
    with open(_log_path, "a", buffering=1) as f:  # line-buffered
        process = subprocess.Popen(
            [python_path, _pyd_config.data.entrypoint],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1, # line-buffered,
            env={**os.environ, "PYTHONUNBUFFERED": "1"}  # if spawning Python subprocesses
        )
        for line in process.stdout:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "line": line.rstrip(),
                "pid": process.pid
            }
            f.write(json.dumps(entry) + "\n")
            f.flush()  # critical — ensures React sees it immediately

        process.wait()
        return process.returncode