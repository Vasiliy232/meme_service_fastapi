__all__ = (
    'get_memes',
    'get_meme',
    'create_meme',
    'get_meme_by_title',
    'delete_meme',
    'update_meme',
)

from sqlalchemy.orm import Session
from models import Meme
from schemas import MemeCreate
from sqlalchemy.exc import DatabaseError
import logging

log = logging.getLogger(__name__)

def get_memes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Meme).offset(skip).limit(limit).all()

def get_meme(db: Session, meme_id: int):
    return db.query(Meme).filter(Meme.id == meme_id).first()

def get_meme_by_title(db: Session, meme_title: str):
    return db.query(Meme).filter(Meme.title == meme_title).first()

def create_meme(db: Session, meme: MemeCreate):
    db_meme = Meme(title=meme.title, description=meme.description, file_id=meme.file_id)
    db.add(db_meme)
    try:
        db.commit()
        db.refresh(db_meme)
        return db_meme
    except DatabaseError:
        log.exception("Could not add meme %s", db_meme)
        db.rollback()

def delete_meme(db: Session, meme: Meme):
    db.delete(meme)
    db.commit()

def update_meme(db: Session, meme: Meme):
    db.commit()
    return meme
