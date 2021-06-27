from pydantic import BaseModel
from typing import List


class GithubUserDTO(BaseModel):
    id: int
    username: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserListDTO(BaseModel):
    github_users: List[GithubUserDTO]
