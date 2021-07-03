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


class GithubUserApproveRequestDto(BaseModel):
    username: str


class GithubUserRenewOneRequestDto(BaseModel):
    username: str


# Response
class GithubUserCreateResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserRetrieveResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserListResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserApproveResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserRenewOneResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str