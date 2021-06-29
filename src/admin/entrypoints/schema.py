from pydantic import BaseModel

# Request
class AdminCreateRequestDto(BaseModel):
    username: str
    password: str
    certification_code: str


# Response
class AdminCreateResponseDto(BaseModel):
    username: str
