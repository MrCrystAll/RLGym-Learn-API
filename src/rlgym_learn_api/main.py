import argparse
import os
import sys
from posixpath import dirname

import uvicorn
from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware

sys.path.append(os.path.join(dirname(__file__), "src"))

from rlgym_learn_api.api.project_router import router as project_router
from rlgym_learn_api.api.run_router import router as run_router
from rlgym_learn_api.api.session_router import router as session_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(project_router)
app.include_router(run_router)
app.include_router(session_router)


@app.get("/")
def ping():
    return Response()


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host="127.0.0.1", port=args.port)
