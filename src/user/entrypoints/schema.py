from pydantic import BaseModel

# Request
class SNSGithubCallbackRequestDto(BaseModel):
    code: str


# Response
class SNSGithubCallbackResponseDto(BaseModel):
    token: str
