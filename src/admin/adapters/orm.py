from datetime import datetime
from sqlalchemy.orm import clear_mappers, mapper
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from src.infra.db.session import metadata
from src.admin.domain.entities.admin import Admin, AdminCertificationCode

admin = Table(
    "admin",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("username", String(length=256), unique=True, nullable=False),
    Column("password", String(length=256), nullable=False),
    Column("created_at", DateTime, default=datetime.now),
    Column("updated_at", DateTime, default=datetime.now, onupdate=datetime.now),
)

admin_certification_code = Table(
    "admin_certification_code",
    metadata,
    Column("code", String(length=256), primary_key=True, unique=True),
    Column("created_at", DateTime, default=datetime.now),
    Column("updated_at", DateTime, default=datetime.now, onupdate=datetime.now),
)


def start_mappers():
    clear_mappers()
    mapper(Admin, admin)
    mapper(AdminCertificationCode, admin_certification_code)
