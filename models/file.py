__all__ = ('File',)

from .database import Base
from sqlalchemy import Column, Integer, String


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    filename = Column(String, index=True)
    s3_url = Column(String)
