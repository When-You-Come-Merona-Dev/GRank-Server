from datetime import timedelta, datetime
import jwt
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


def jwt_payload_handler(user: Admin) -> dict:
    payload = {
        "scope": "access_token",
        "sub": user.username,
        "iss": CONFIG.DOMAIN,
        "exp": int((datetime.utcnow() + timedelta(days=3)).timestamp()),
        "iat": int(datetime.utcnow().timestamp()),
        "username": user.username,
        "id": user.id,
    }
    return payload
