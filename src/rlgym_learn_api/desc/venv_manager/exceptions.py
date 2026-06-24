from rlgym_learn_api.desc.exception import RLGymLearnApiException


class VenvCreationFailed(RLGymLearnApiException):
    """Exception thrown when a virtual environment fails to create itself"""

    def __init__(self, description: str, error_code: int) -> None:
        super().__init__("Virtual environment creation failed", description, error_code)


class VenvDeletionFailed(RLGymLearnApiException):
    """Exception thrown when a virtual environment fails to delete itself"""

    def __init__(self, description: str, error_code: int) -> None:
        super().__init__("Virtual environment deletion failed", description, error_code)


class VenvDoesntExist(RLGymLearnApiException):
    """Exception thrown when a project doesnt have a virtual environment but tries to act as if it has one."""

    def __init__(self, description: str) -> None:
        super().__init__("Virtual environment doesn't exist", description, 404)


class PackageExists(RLGymLearnApiException):
    """Exception thrown when a venv already has a package but is trying to install it again"""

    def __init__(self, description: str) -> None:
        super().__init__("Package already exists.", description, 409)


class VenvCommandFailed(RLGymLearnApiException):
    """Exception thrown when a venv command fails unexpectedly"""

    def __init__(self, title: str, description: str, error_code: int) -> None:
        super().__init__(title, description, error_code)
