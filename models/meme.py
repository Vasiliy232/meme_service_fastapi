__all__ = ('Meme',)

from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .file import File


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))

    file = relationship("File", backref="memes")

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"{__class__.__name__}: {self.description}\n"
                f"file_id: {self.file_id}\n"
                "------------")

    def __repr__(self):
        return str(self)