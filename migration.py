"""
This is an "automatic" migration guide, allows the user to automatically update their project
Requires a project ID and a root folder
"""

import json
import os
import sys
from argparse import ArgumentParser

from packaging.version import parse

from rlgym_learn_api import __version__
from rlgym_learn_api.desc.project.project import AdvancedConfigModel, ProjectMetadata

if __name__ == "__main__":
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--project-id", "-pid", help="The ID of the project to migrate"
    )
    arg_parser.add_argument("--root", "-r", help="The root folder where the project is")

    args = arg_parser.parse_args()

    _pid = args.project_id
    _root = args.root

    _path = os.path.join(_root, _pid)

    if not os.path.exists(_path):
        print(f"Project {_pid} doesn't exist at path {_root}", file=sys.stderr)
        sys.exit(1)

    _config_path = os.path.join(_path, "project_config.json")

    if not os.path.exists(_config_path):
        print(
            f"Config doesn't exist in project {_pid} located at {_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(_config_path, "r") as config_file:
        _config = json.load(config_file)

    # ---------------- Version assertion ----------------
    if "created_at_version" not in _config:
        _config["created_at_version"] = (
            "0.1.5"  # 0.1.6-dev.1 is when "created_at_version" got implemented, so i go to the previous patch
        )

    _project_version = parse(_config["created_at_version"])
    _api_version = parse(__version__)

    # Implemented in 0.1.7-dev.6
    if "advanced_config" not in _config:
        _config["advanced_config"] = AdvancedConfigModel().model_dump()

    # If same version than API, ignore and quit
    if _project_version == _api_version:
        print(
            f"Project {_pid} is up to date with the API (Current version: {_api_version})"
        )
        sys.exit(2)

    elif _project_version > _api_version:
        print(
            f"The project was created in version {_project_version} while the API is in version {_api_version}. Please update the API."
        )
        sys.exit(1)

    _invalid_api_version = False

    # Overwrite the project config to apply changes
    with open(_config_path, "w") as config_file:
        _validated_config = ProjectMetadata.model_validate(_config)
        _validated_config.created_at_version = str(_api_version)

        json.dump(_validated_config.model_dump(), config_file)

    print(
        f"Project {_pid} successfully migrated from version {_project_version} to project {_validated_config.created_at_version}"
    )
