from dataclasses import dataclass
from os import environ


@dataclass
class Config:
    API_ENV: str = environ.get("API_ENV", "develop")

    DATABASE_USER: str = environ.get("POSTGRES_USER", "root")
    DATABASE_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "password")
    DATABASE_HOST: str = environ.get("POSTGRES_HOST", "db")
    DATABASE_PORT: int = int(environ.get("POSTGRES_PORT", 5432))
    DATABASE_NAME: str = environ.get("POSTGRES_NAME", "wycm_dev_db")
    DATABASE_URL: str = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
        DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
    )

    DEBUG: bool = False
    TEST_MODE: bool = False
    PROJ_RELOAD: bool = True
    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY", "thisissecretkey!@#$")
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM", "HS256")
    WEB_SERVER_HOST: str = environ.get("WEB_SERVER_HOST", "0.0.0.0")
    WEB_SERVER_PORT: int = int(environ.get("WEB_SERVER_PORT", 3052))

    PAGINATION_PER_PAGE: int = int(environ.get("PAGINATION_PER_PAGE", 5))

    JWT_SECRET_KEY: str = environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = environ.get("JWT_ALGORITHM", "HS256")

    DOMAIN: str = environ.get("DOMAIN", "localhost:3052")

    GITHUB_API_TOKEN: str = environ.get("GITHUB_API_TOKEN", None)
    GITHUB_API_CLIENT_ID: str = environ.get("GITHUB_API_CLIENT_ID", None)
    GITHUB_API_CLIENT_SECRET: str = environ.get("GITHUB_API_CLIENT_SECRET", None)
    GITHUB_OAUTH_REDIRECT_URI: str = environ.get("GITHUB_OAUTH_REDIRECT_URI", None)


@dataclass
class DevelopConfig(Config):
    PROJ_RELOAD = True
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    DEBUG: bool = True


@dataclass
class ProductConfig(Config):
    PROJ_RELOAD = False
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]


@dataclass
class TestConfig(Config):
    TRUSTED_HOSTS = ["*"]
    ALLOW_SITE = ["*"]
    TEST_MODE: bool = True


def load_config() -> Config:
    config = dict(product=ProductConfig, develop=DevelopConfig, test=TestConfig)
    return config[environ.get("API_ENV", "develop")]()


CONFIG = load_config()
