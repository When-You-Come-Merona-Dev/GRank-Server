from dataclasses import dataclass
from os import environ


@dataclass
class Config:
    API_ENV: str = environ.get("API_ENV", "local")
    DEBUG: bool = False
    TEST_MODE: bool = False
    PROJ_RELOAD = True
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY", "thisissecretkey!@#$")
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM", "HS256")
    WEB_SERVER_HOST: str = environ.get("WEB_SERVER_HOST", "0.0.0.0")
    WEB_SERVER_PORT: int = int(environ.get("WEB_SERVER_PORT", 3052))


@dataclass
class LocalConfig(Config):
    DATABASE_NAME = environ.get("LOCAL_DB_NAME", "test")
    DATABASE_HOST = environ.get("LOCAL_DB_HOST", "localhost")
    DATABASE_PASSWORD = environ.get("LOCAL_DB_PASSWORD", "")
    DATABASE_USER = environ.get("LOCAL_DB_USER", "root")
    DATABASE_PORT = int(environ.get("LOCAL_DB_PORT", 3306))
    PROJ_RELOAD = True
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProdConfig(Config):
    DATABASE_NAME = environ.get("PROD_DB_NAME", "test")
    DATABASE_HOST = environ.get("PROD_DB_HOST", "localhost")
    DATABASE_PASSWORD = environ.get("PROD_DB_PASSWORD", "")
    DATABASE_USER = environ.get("PROD_DB_USER", "root")
    DATABASE_PORT = int(environ.get("PROD_DB_PORT", 3306))
    PROJ_RELOAD = False
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def load_config():
    config = dict(prod=ProdConfig, local=LocalConfig, test=TestConfig)
    return config[environ.get("API_ENV", "local")]()


config = load_config()