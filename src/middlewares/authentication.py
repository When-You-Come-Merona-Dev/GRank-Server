from typing import Optional, Tuple
import jwt
from starlette.authentication import AuthenticationBackend, BaseUser
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from src.utils.token_handlers import jwt_decode_handler


class CustomUser(BaseUser):
    def __init__(self, username: str, is_admin: bool) -> None:
        self.username = username
        self.is_admin = is_admin

    @property
    def is_authenticated(self) -> bool:
        return True


class JWTAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, conn) -> Optional[Tuple[bool, CustomUser]]:
        authorization: str = conn.headers.get("Authorization")

        if not authorization:
            return False, None
        try:
            token_type, token = authorization.split(" ")
            if token_type.lower() not in ("jwt", "bearer"):
                return False, None
        except ValueError:
            return False, None

        if not token:
            return False, None

        try:
            payload = jwt_decode_handler(token)
        except jwt.PyJWTError as exe:
            return False, None
        user = CustomUser(username=payload["username"], is_admin=payload["is_admin"])
        return True, user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass