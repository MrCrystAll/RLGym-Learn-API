import json
import os
import pathlib
import shutil

from void_api.common_values import PROJECT_CONFIG_JSON_FILE
from void_api.primitives import Project

def generate_entrypoint(path: str | os.PathLike[str], project: Project):
    _path = pathlib.Path(os.path.join(path, "main.py"))
    if _path.exists():
        raise OSError(f"There is already an entrypoint for the project {project.metadata.name}")
    
    shutil.copy(os.path.join("rlgym_learn_utils", "entrypoint.py"), _path)
    
    project.data.entrypoint = str(_path)
    
def generate_log_folder(project: Project):
    _stdout_log_path = pathlib.Path(project.data.log_config.stdout_log)
    
    os.makedirs(_stdout_log_path.parent, exist_ok=False)
    _stdout_log_path.touch(exist_ok=False)

def generate_project_directory(path: str | os.PathLike[str], project: Project):
    _path = pathlib.Path(path)
    os.makedirs(_path, exist_ok=False)
    generate_entrypoint(_path, project)
    generate_log_folder(project)
    with open(_path / PROJECT_CONFIG_JSON_FILE, "x") as f:
        json.dump(
            project.model_dump(),
            f
        )