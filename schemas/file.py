__all__ = (
    'FileCreate',
    'File',
    'FileBase',
)

from pydantic import BaseModel
from typing import List
from .meme import Meme


class FileBase(BaseModel):
    filename: str
    s3_url: str


class FileCreate(FileBase):
    pass

class File(FileBase):
    id: int
    memes: List[Meme] = []

    class Config:
        from_attributes = True
