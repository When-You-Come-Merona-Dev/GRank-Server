from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Table, MetaData
from sqlalchemy.orm import mapper, relationship
from sqlalchemy.sql.schema import ForeignKey
from src.adapters.db.session import metadata
from src.domain.entities.github_user import GithubUser
from src.domain.entities.group import Group


github_user = Table(
    "github_user",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("username", String(length=256), unique=True, nullable=False),
    Column("commit_count", Integer, default=0, nullable=False),
    Column("is_approved", Boolean, default=False, nullable=False),
    Column("created_at", DateTime, default=datetime.now),
    Column("updated_at", DateTime, default=datetime.now, onupdate=datetime.now),
)

group = Table(
    "group",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("name", String(length=256), nullable=False),
    Column("category", String(length=256), nullable=False),
)

github_user_group = Table(
    "github_user_group",
    metadata,
    Column("github_user_id", Integer, ForeignKey("github_user.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("group.id"), primary_key=True),
)


def start_mappers():
    mapper(
        GithubUser,
        github_user,
        properties={
            "groups": relationship("group", secondary=github_user_group, back_populates="members")
        },
    )
    mapper(Group, group)