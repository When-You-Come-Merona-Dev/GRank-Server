import secrets
import bcrypt


def get_hasher(algorithm: str = "default"):
    if algorithm == "default":
        return BcryptSHA256PasswordHasher()

    raise ValueError("Not found algorithm")


def get_random_alphabet(length: int = 12) -> str:
    ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    return "".join(secrets.choice(ALPHABET) for i in range(length))


def hash_password(raw_password: str, salt: str = None, algorithm: str = "default") -> str:
    hasher = get_hasher(algorithm)
    if salt is None:
        salt = hasher.generate_salt()

    encoded = hasher.encode(raw_password, salt)
    return encoded


def check_password(password: str, encoded: str, preferred="default") -> bool:
    hasher = get_hasher(preferred)
    is_correct = hasher.verify(password, encoded)
    return is_correct


class BasePasswordHasher:
    algorithm = None

    def generate_salt(self):
        return get_random_alphabet(12)

    def encode(self, raw_password, salt):
        raise NotImplementedError("You must override encode method")

    def verify(self, password, encoded):
        raise NotImplementedError("You must override verify method")


class BcryptSHA256PasswordHasher(BasePasswordHasher):
    algorithm = "bcrypt_sha256"
    rounds = 12

    def generate_salt(self):
        return bcrypt.gensalt(self.rounds)

    def encode(self, password: str, salt: str):
        password = password.encode("utf-8")
        encoded = bcrypt.hashpw(password, salt)
        return encoded.decode()

    def verify(self, password: str, encoded: str):
        password = password.encode("utf-8")
        encoded = encoded.encode("utf-8")
        return bcrypt.checkpw(password, encoded)
