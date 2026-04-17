import os
from posixpath import dirname
import sys

from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware

sys.path.append(
    os.path.join(dirname(__file__), "src")
)

from void_api.api.api_crud_primitives import ProjectCreationArgs, ProjectCreationReturn, ProjectsFetchArgs, ProjectsFetchReturn
from void_api.crud_operations import create_project, get_all_projects

from void_api.routers.project_router import router as project_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router)

@app.get("/")
def ping():
    return Response()

@app.post("/create")
def api_create_project(args: ProjectCreationArgs):
    try:
        _project = create_project(args.path, args.metadata)
        return ProjectCreationReturn(
            project=_project
        )
    except OSError:
        return Response(f"A project with the name {args.metadata.name} already exists at path {args.path}", status_code=409)
    
@app.post("/all")
def api_get_all_projects(args: ProjectsFetchArgs) -> ProjectsFetchReturn:
    _projects = get_all_projects(args.path)
    
    return ProjectsFetchReturn(projects=_projects)