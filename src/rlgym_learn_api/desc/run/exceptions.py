from rlgym_learn_api.desc.exception import (
    RLGymLearnApiException,
    RLGymLearnApiExceptionModel,
)


class RunNotFoundErrorModel(RLGymLearnApiExceptionModel):
    run_name: str


class RunNotFoundError(RLGymLearnApiException[RunNotFoundErrorModel]):
    def __init__(self, run_name: str) -> None:
        super().__init__(f"Run {run_name} doesn't exist", 404)
        self._run_name = run_name

    def to_dict(self) -> RunNotFoundErrorModel:
        return RunNotFoundErrorModel(message=self.message, run_name=self._run_name)


class RunAlreadyExistsErrorModel(RLGymLearnApiExceptionModel):
    run_name: str


class RunAlreadyExistsError(RLGymLearnApiException[RunAlreadyExistsErrorModel]):
    def __init__(self, run_name: str) -> None:
        super().__init__(f"Run {run_name} already exists", 409)
        self._run_name = run_name

    def to_dict(self) -> RunAlreadyExistsErrorModel:
        return RunAlreadyExistsErrorModel(message=self.message, run_name=self._run_name)


class UnknownConfigTypeModel(RLGymLearnApiExceptionModel):
    config_type: str


class UnknownConfigType(RLGymLearnApiException[UnknownConfigTypeModel]):
    def __init__(self, config_type: str) -> None:
        super().__init__("Unknown config type", 417)
        self._config_type = config_type

    def to_dict(self) -> UnknownConfigTypeModel:
        return UnknownConfigTypeModel(
            message=self.message, config_type=self._config_type
        )


class RunConfigMissingErrorModel(RLGymLearnApiExceptionModel):
    run_name: str


class RunConfigMissingError(RLGymLearnApiException[RunConfigMissingErrorModel]):
    def __init__(self, run_name: str) -> None:
        super().__init__(f"Config is missing for run {run_name}", 417)
        self._run_name = run_name

    def to_dict(self) -> RunConfigMissingErrorModel:
        return RunConfigMissingErrorModel(message=self.message, run_name=self._run_name)
