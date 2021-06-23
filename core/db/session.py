from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core.config import config
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(config.DATABASE_URL)

LocalSession = scoped_session(sessionmaker(bind=engine))

BaseORM = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
