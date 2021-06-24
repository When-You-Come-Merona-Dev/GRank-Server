from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from src.config import config


engine = create_engine(config.DATABASE_URL)

LocalSession = scoped_session(sessionmaker(bind=engine))

metadata = MetaData()


def get_session():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
