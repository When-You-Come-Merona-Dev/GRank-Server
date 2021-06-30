from typing import Optional, Tuple
import jwt
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from src.utils.token_handlers import jwt_decode_handler
from starlette.authentication import SimpleUser


class JWTAuthenticationBackend(AuthenticationBackend):
    async def authenticate(self, conn) -> Optional[Tuple[bool, SimpleUser]]:
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
        user = SimpleUser(username=payload["username"])
        return True, user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass