import json
import os
import pathlib
import shutil

from void_api.common_values import PROJECT_CONFIG_JSON_FILE
from void_api.primitives import Project
from void_api.reward_file_generator import generate_rewards_file

def generate_entrypoint(path: str | os.PathLike[str], project: Project):
    _path = pathlib.Path(os.path.join(path, "main.py"))
    if _path.exists():
        raise OSError(f"There is already an entrypoint for the project {project.metadata.name}")
    
    shutil.copy("entrypoint.py", _path)
    
    project.data.entrypoint = str(_path)

def generate_project_directory(path: str, project: Project):
    _path = pathlib.Path(path)
    os.makedirs(_path, exist_ok=False)
    generate_rewards_file(_path, project)
    generate_entrypoint(_path, project)
    with open(_path / PROJECT_CONFIG_JSON_FILE, "x") as f:
        json.dump(
            project.model_dump(),
            f
        )