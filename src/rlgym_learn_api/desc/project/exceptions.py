from rlgym_learn_api.desc.exception import (
    RLGymLearnApiException,
    RLGymLearnApiExceptionModel,
)


class ProjectNotFoundErrorModel(RLGymLearnApiExceptionModel):
    inner_message: str | None
    project_id: str


class ProjectNotFoundError(RLGymLearnApiException[ProjectNotFoundErrorModel]):
    """An exception thrown when a project is not found, carries an inner message to get more details about the error"""

    def __init__(self, project_id: str, inner_message: str | None = None) -> None:
        super().__init__("Project not found", 404)
        self._inner_message = inner_message
        self._project_id = project_id

    def to_dict(self) -> ProjectNotFoundErrorModel:
        return ProjectNotFoundErrorModel(
            message=self.message,
            inner_message=self._inner_message,
            project_id=self._project_id,
        )


class ProjectCreationFailedModel(RLGymLearnApiExceptionModel):
    name: str
    inner_exception_message: str


class ProjectCreationFailed(RLGymLearnApiException[ProjectCreationFailedModel]):
    """An exception thrown when a project fails to create, carries an inner exception for more details"""

    def __init__(self, name: str, error_code: int, inner_exception: Exception) -> None:
        super().__init__(
            message=f'Project "{name}" creation failed',
            error_code=error_code,
        )
        self._name = name
        self._inner_exception = inner_exception

    def to_dict(self) -> ProjectCreationFailedModel:
        return ProjectCreationFailedModel(
            message=self.message,
            inner_exception_message=str(self._inner_exception),
            name=self._name,
        )


class ProjectMalformedModel(RLGymLearnApiExceptionModel):
    project_id: str
    inner_message: str | None


class ProjectMalformed(RLGymLearnApiException[ProjectMalformedModel]):
    """An exception thrown if a project doesn't match with the expected schema, contains an inner message for more details"""

    def __init__(self, project_id: str, inner_message: str | None) -> None:
        super().__init__(error_code=417, message=f"Project {project_id} is malformed")
        self._inner_message = inner_message
        self._project_id = project_id

    def to_dict(self) -> ProjectMalformedModel:
        return ProjectMalformedModel(
            message=self.message,
            inner_message=self._inner_message,
            project_id=self._project_id,
        )


class ProjectRootFolderNotFoundModel(RLGymLearnApiExceptionModel):
    path: str


class ProjectRootFolderNotFound(RLGymLearnApiException[ProjectRootFolderNotFoundModel]):
    def __init__(self, path: str) -> None:
        super().__init__(message="Project root folder not found", error_code=404)
        self._path = path

    def to_dict(self) -> ProjectRootFolderNotFoundModel:
        return ProjectRootFolderNotFoundModel(message=self.message, path=self._path)
