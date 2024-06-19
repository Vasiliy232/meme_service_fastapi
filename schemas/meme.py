__all__ = (
    'MemeCreate',
    'Meme',
)

from pydantic import BaseModel
from typing import Union
from fastapi import Form


class MemeBase(BaseModel):
    title: str
    description: Union[str, None] = None
    file_id: Union[int, None] = None


class MemeCreate(MemeBase):
    
    @classmethod
    def as_form(cls, title: str = Form(...), description: str = Form("")):
        return cls(title=title, description=description)


class Meme(MemeBase):
    id: int

    class Config:
        from_attributes = True
