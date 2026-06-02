from rlgym_learn_api.desc.exception import RLGymLearnApiException


class ProjectNotFoundError(RLGymLearnApiException):
    """An exception thrown when a project is not found, carries an inner message to get more details about the error"""

    def __init__(self, description: str, project_id: str) -> None:
        super().__init__(f"Project {project_id} not found", description, 404)


class ProjectCreationFailed(RLGymLearnApiException):
    """An exception thrown when a project fails to create, carries an inner exception for more details"""

    def __init__(self, description: str, project_name: str, error_code: int) -> None:
        super().__init__(
            title=f'Project "{project_name}" creation failed',
            description=description,
            error_code=error_code,
        )


class ProjectMalformed(RLGymLearnApiException):
    """An exception thrown if a project doesn't match with the expected schema, contains an inner message for more details"""

    def __init__(self, description: str, project_id: str) -> None:
        super().__init__(
            error_code=417,
            title=f"Project {project_id} is malformed",
            description=description,
        )


class ProjectRootFolderNotFound(RLGymLearnApiException):
    def __init__(self, description: str, path: str) -> None:
        super().__init__(
            title=f'Project root folder (Evaluated at "{path}") not found',
            description=description,
            error_code=404,
        )
