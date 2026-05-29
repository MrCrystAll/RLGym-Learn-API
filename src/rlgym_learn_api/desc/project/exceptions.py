from typing import Any

from rlgym_learn_api.desc.exception import RLGymLearnApiException


class ProjectNotFoundError(RLGymLearnApiException):
    """An exception thrown when a project is not found, carries an inner message to get more details about the error"""

    def __init__(self, project_id: str, inner_message: str | None = None) -> None:
        super().__init__("Project not found", 404)
        self._inner_message = inner_message
        self._project_id = project_id

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict() | {
            "inner_message": self._inner_message,
            "project_id": self._project_id,
        }


class ProjectCreationFailed(RLGymLearnApiException):
    """An exception thrown when a project fails to create, carries an inner exception for more details"""

    def __init__(self, name: str, error_code: int, inner_exception: Exception) -> None:
        super().__init__(
            message=f'Project "{name}" creation failed due to the following error: {str(inner_exception)}',
            error_code=error_code,
        )
        self._inner_exception = inner_exception

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict() | {"exception": str(self._inner_exception)}


class ProjectMalformed(RLGymLearnApiException):
    """An exception thrown if a project doesn't match with the expected schema, contains an inner message for more details"""

    def __init__(self, project_id: str, inner_message: str | None) -> None:
        super().__init__(error_code=417, message=f"Project {project_id} is malformed")
        self._inner_message = inner_message
        self._project_id = project_id

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict() | {
            "inner_message": self._inner_message,
            "project_id": self._project_id,
        }


class ProjectRootFolderNotFound(RLGymLearnApiException):
    def __init__(self, path: str) -> None:
        super().__init__(message="Project root folder not found", error_code=404)
        self._path = path

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict() | {"path": self._path}
