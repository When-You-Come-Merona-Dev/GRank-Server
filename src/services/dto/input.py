from pydantic import BaseModel


class AddGithubUserDTO(BaseModel):
    username: str
    commit_count: int
