from pydantic import BaseModel


class GithubUserDTO(BaseModel):
    id: int
    username: str
    commit_count: int
    is_approved: bool
    groups: set
