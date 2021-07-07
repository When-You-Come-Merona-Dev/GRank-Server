from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from src.config import CONFIG


engine = create_engine(CONFIG.DATABASE_URL)

sqlalchemy_session_factory = sessionmaker(bind=engine)

metadata = MetaData()
