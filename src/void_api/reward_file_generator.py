from os import PathLike
import os.path
import pathlib

from void_api.primitives import Project


def generate_rewards_file(path: str | PathLike[str], project: Project):
    _path = pathlib.Path(os.path.join(path, "rewards.py"))
    _path.touch(exist_ok=False)
    project.data.rewards_files.append(str(_path))