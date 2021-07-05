from datetime import datetime
from sqlalchemy import Column, String, Integer, Table, DateTime
from sqlalchemy.orm import mapper
from src.infra.db.session import metadata
from src.user.domain.entities.user import User


user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("github_id", String(length=256), nullable=False),
    Column("password", String(length=256), nullable=False),
    Column("created_at", DateTime, default=datetime.now),
    Column("updated_at", DateTime, default=datetime.now, onupdate=datetime.now),
)


def start_mappers():
    mapper(User, user)
