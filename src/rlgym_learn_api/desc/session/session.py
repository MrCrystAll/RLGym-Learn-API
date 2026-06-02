from pydantic import BaseModel


class LogConfig(BaseModel):
    stdout: str
    stderr: str


class Session(BaseModel):
    session_id: str
    project_id: str
    run_name: str

    status: str
    logs: LogConfig

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Session):
            return False

        return self.session_id == value.session_id
