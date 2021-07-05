from typing import Union
from datetime import timedelta, datetime
import jwt
from src.user.domain.entities.user import User
from src.admin.domain.entities.admin import Admin
from src.config import CONFIG


def jwt_encode_handler(payload) -> str:
    key = CONFIG.JWT_SECRET_KEY
    algorithm = CONFIG.JWT_ALGORITHM

    return jwt.encode(dict(payload), key, algorithm)


def jwt_decode_handler(token: str) -> dict:
    token = token.encode()
    key = CONFIG.JWT_SECRET_KEY
    algorithm = CONFIG.JWT_ALGORITHM
    decoded = jwt.decode(token, key, algorithm)
    return decoded


def jwt_payload_handler(user: Union[Admin, User]) -> dict:
    payload = {}
    if isinstance(user, Admin):
        payload = {
            "scope": "access_token",
            "sub": user.username,
            "iss": CONFIG.DOMAIN,
            "exp": int((datetime.utcnow() + timedelta(days=3)).timestamp()),
            "iat": int(datetime.utcnow().timestamp()),
            "username": user.username,
            "is_admin": True,
            "id": user.id,
        }
    elif isinstance(user, User):
        payload = {
            "scope": "access_token",
            "sub": user.github_id,
            "iss": CONFIG.DOMAIN,
            "exp": int((datetime.utcnow() + timedelta(days=3)).timestamp()),
            "iat": int(datetime.utcnow().timestamp()),
            "is_admin": False,
            "id": user.id,
        }

    return payload
