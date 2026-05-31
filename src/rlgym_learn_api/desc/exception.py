from abc import abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


class RLGymLearnApiExceptionModel(BaseModel):
    message: str


ExceptionModelTypeVar = TypeVar(
    "ExceptionModelTypeVar", bound=RLGymLearnApiExceptionModel
)


class RLGymLearnApiException(Exception, Generic[ExceptionModelTypeVar]):
    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(message, error_code)
        self.message = message
        self.error_code = error_code

    @abstractmethod
    def to_dict(self) -> ExceptionModelTypeVar:
        pass
