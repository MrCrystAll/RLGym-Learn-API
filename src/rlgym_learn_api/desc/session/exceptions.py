from rlgym_learn_api.desc.exception import RLGymLearnApiException


class SessionNotFoundError(RLGymLearnApiException):
    def __init__(self, session_id: str, description: str) -> None:
        super().__init__(f"Session {session_id} doesn't exist", description, 404)
