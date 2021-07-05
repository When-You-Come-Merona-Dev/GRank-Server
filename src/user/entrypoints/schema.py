from pydantic import BaseModel

# Request
class SNSGithubCallbackRequestDto(BaseModel):
    code: str


# Response
class SNSGithubCallbackResponseDto(BaseModel):
    id: int
    username: str
    avatar_url: str
    commit_count: int
    is_approved: bool
    groups: set
    created_at: str
    updated_at: str