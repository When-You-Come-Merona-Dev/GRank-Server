from typing import Optional
from pydantic import BaseModel

# Request
class GithubUserCreateRequestDto(BaseModel):
    username: str


class GithubUserListRequestDto(BaseModel):
    filters: Optional[dict]
    page: Optional[int]
    per_page: Optional[int]
    order_by: Optional[str]


# Response
class GithubUserCreateResponseDto(BaseModel):
    id: int
    username: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserRetrieveResponseDto(BaseModel):
    id: int
    username: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserListResponseDto(BaseModel):
    id: int
    username: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str