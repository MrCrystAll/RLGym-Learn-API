from rlgym_learn_api.desc.exception import RLGymLearnApiException


class VenvCreationFailed(RLGymLearnApiException):
    """Exception thrown when a virtual environment fails to create itself"""

    def __init__(self, description: str, error_code: int) -> None:
        super().__init__("Virtual environment creation failed", description, error_code)


class VenvDeletionFailed(RLGymLearnApiException):
    """Exception thrown when a virtual environment fails to delete itself"""

    def __init__(self, description: str, error_code: int) -> None:
        super().__init__("Virtual environment deletion failed", description, error_code)
