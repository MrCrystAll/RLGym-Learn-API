import os
from posixpath import dirname
import sys

from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware

sys.path.append(os.path.join(dirname(__file__), "src"))

from void_api.api.project_router import router as project_router
from void_api.api.run_router import router as run_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router)
app.include_router(run_router)


@app.get("/")
def ping():
    return Response()
