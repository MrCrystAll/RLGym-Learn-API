from rlgym_learn_api.desc.exception import (
    RLGymLearnApiException,
)


class RunNotFoundError(RLGymLearnApiException):
    def __init__(self, description: str, run_name: str) -> None:
        super().__init__(
            title=f"Run {run_name} not found", description=description, error_code=404
        )


class RunAlreadyExistsError(RLGymLearnApiException):
    def __init__(self, description: str, run_name: str) -> None:
        super().__init__(f"Run {run_name} already exists", description, 409)


class UnknownConfigType(RLGymLearnApiException):
    def __init__(self, description: str, config_type: str) -> None:
        super().__init__("Unknown config type", description, 417)


class RunConfigMissingError(RLGymLearnApiException):
    def __init__(self, description: str, run_name: str) -> None:
        super().__init__(f"Config is missing for run {run_name}", description, 417)
