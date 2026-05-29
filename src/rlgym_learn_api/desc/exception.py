from typing import Any


class RLGymLearnApiException(Exception):
    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(message, error_code)
        self.message = message
        self.error_code = error_code

    def to_dict(self) -> dict[str, Any]:
        return {"reason": self.message}
