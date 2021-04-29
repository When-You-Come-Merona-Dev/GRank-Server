from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from core.config import config


engine = create_engine(config.DATABASE_URL)

Session = scoped_session(sessionmaker(bind=engine))

session = Session()
