from abc import abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


class RLGymLearnApiExceptionModel(BaseModel):
    title: str
    description: str


ExceptionModelTypeVar = TypeVar(
    "ExceptionModelTypeVar", bound=RLGymLearnApiExceptionModel
)


class RLGymLearnApiException(Exception, Generic[ExceptionModelTypeVar]):
    def __init__(self, title: str, description: str, error_code: int) -> None:
        super().__init__(title, description, error_code)
        self.title = title
        self.description = description
        self.error_code = error_code

    def to_dict(self) -> ExceptionModelTypeVar:
        return RLGymLearnApiExceptionModel(
            title=self.title, description=self.description
        )
