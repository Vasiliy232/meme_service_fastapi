__all__ = (
    'Base',
    'db_session',
    'engine',
)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URI = getenv(
    "SQLALCHEMY_DATABASE_URI",
    'postgresql+psycopg2://user:password@localhost:5432/meme'
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
