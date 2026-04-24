from pydantic import BaseModel


class Run(BaseModel):
    # A run is attached to a project
    project_id: str

    # The name is the id
    name: str

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Run):
            return False
        return self.name == value.name
