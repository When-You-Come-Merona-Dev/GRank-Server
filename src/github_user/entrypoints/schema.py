from typing import Optional
from pydantic import BaseModel

# Request
class GithubUserCreateRequestDto(BaseModel):
    username: str


class GithubUserRetrieveRequestDto(BaseModel):
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


class GithubUserRenewAllRequestDto(BaseModel):
    pass


class GithubUserPartialUpdateRequestDto(BaseModel):
    grade: Optional[int]
    is_public: Optional[bool]


class GithubUserDeleteRequestDto(BaseModel):
    username: str


class SNSGithubCallbackRequestDto(BaseModel):
    code: str


# Response
class GithubUserCreateResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    grade: int
    is_public: bool
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserRetrieveResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    grade: int
    is_public: bool
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserListResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    grade: int
    is_public: bool
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserApproveResponseDto(BaseModel):
    detail: str


class GithubUserRenewOneResponseDto(BaseModel):
    detail: str


class GithubUserRenewAllResponseDto(BaseModel):
    detail: str


class GithubUserPartialUpdateResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    grade: int
    is_public: bool
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str


class GithubUserDeleteResponseDto(BaseModel):
    detail: str


class SNSGithubCallbackResponseDto(BaseModel):
    token: str
