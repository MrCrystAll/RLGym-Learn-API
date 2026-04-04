import os
import pathlib
import shutil

from void_api.common_values import PROJECT_CONFIG_JSON_FILE
from void_api.primitives import Project, ProjectData, ProjectMetadata
from void_api.project_directory_generator import generate_project_directory


def create_project(path: str, metadata: ProjectMetadata):
    _folder_path = os.path.join(
        path, metadata.name.replace(" ", "_").lower()
    )
    
    metadata.path = _folder_path
    
    project = Project(
        metadata=metadata,
        data=ProjectData(
            rewards_files=[],
            entrypoint=""
        )
    )
    
    generate_project_directory(_folder_path, project)
    
    return project


def get_all_projects(path: str) -> list[ProjectMetadata]:
    _projects = []
    
    for file in os.listdir(path):
        _path = pathlib.Path(
            os.path.join(path, file)
        )
        
        if not _path.is_dir():
            continue
        
        if not (_path / PROJECT_CONFIG_JSON_FILE).exists():
            continue
        
        _project_meta = Project.model_validate_json((_path / PROJECT_CONFIG_JSON_FILE).read_text()).metadata
        _projects.append(_project_meta)
        
    return _projects

def get_project_details(metadata: ProjectMetadata) -> ProjectData:
    assert metadata.path is not None, "Can't find project data if no path"
    
    _path = pathlib.Path(metadata.path)
    _config = _path / PROJECT_CONFIG_JSON_FILE
    
    return Project.model_validate_json(_config.read_text()).data


def delete_project(metadata: ProjectMetadata):
    assert metadata.path is not None, "Can't delete project if no path"
    
    shutil.rmtree(metadata.path, False)