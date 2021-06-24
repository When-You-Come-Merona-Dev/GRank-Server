from pydantic import BaseModel


class AddGithubUserDTO(BaseModel):
    username: str
