from pydantic import BaseModel

# Request
class AdminCreateRequestDto(BaseModel):
    username: str
    password: str
    certification_code: str


class AdminLoginRequestDto(BaseModel):
    username: str
    password: str


# Response
class AdminCreateResponseDto(BaseModel):
    username: str


class AdminLoginResponseDto(BaseModel):
    token: str
