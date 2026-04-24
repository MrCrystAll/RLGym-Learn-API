import json
import os
import pathlib
import shutil

from rlgym_learn.learning_coordinator_config import (
    LearningCoordinatorConfigModel,
    SerdeTypesModel,
    BaseConfigModel,
)
from rlgym_learn.rlgym_learn import PyAnySerdeType

import numpy as np


def generate_entrypoint(path: str | os.PathLike[str]):
    _path = pathlib.Path(path)

    # Create directory in case the entrypoint is nested
    os.makedirs(_path.parent, exist_ok=True)
    shutil.copy(os.path.join("rlgym_learn_utils", "entrypoint.py"), _path)


def generate_log_folder(path: str | os.PathLike[str]):
    os.makedirs(path, exist_ok=False)


def generate_runs_folder(path: str | os.PathLike[str]):
    _path = pathlib.Path(path) / "runs"
    os.makedirs(_path, exist_ok=False)
    (_path / "runs.json").write_text(json.dumps([]))


def generate_config(path: str | os.PathLike[str]):
    _path = pathlib.Path(path)

    # Create directory in case the config is nested
    os.makedirs(_path.parent, exist_ok=True)
    _path.write_text(
        LearningCoordinatorConfigModel(
            base_config=BaseConfigModel(
                serde_types=SerdeTypesModel(
                    agent_id_serde_type=PyAnySerdeType.STRING(),
                    action_serde_type=PyAnySerdeType.NUMPY(np.int64),
                    obs_serde_type=PyAnySerdeType.NUMPY(np.float64),
                    reward_serde_type=PyAnySerdeType.FLOAT(),
                    obs_space_serde_type=PyAnySerdeType.TUPLE(
                        (PyAnySerdeType.STRING(), PyAnySerdeType.INT())
                    ),
                    action_space_serde_type=PyAnySerdeType.TUPLE(
                        (PyAnySerdeType.STRING(), PyAnySerdeType.INT())
                    ),
                ),
            )
        ).model_dump_json()
    )


def generate_project_directory(path: str):

    # Structure
    # - ID
    # ---- config.json
    # ---- logs
    # ---- src
    # ------- config.json
    # ------- main.py

    _path = pathlib.Path(path) / "src"
    os.makedirs(_path, exist_ok=False)
    generate_entrypoint(str(_path / "main.py"))
    generate_log_folder(str(_path / ".." / "logs"))
    generate_config(_path / "config.json")
    generate_runs_folder(str(path))
