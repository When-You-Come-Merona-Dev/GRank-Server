from pydantic import BaseModel

# Request
class GithubUserCreateRequestDto(BaseModel):
    username: str


class GithubUserListRequestDto(BaseModel):
    filters: dict
    page: int
    per_page: int
    order_by: str


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