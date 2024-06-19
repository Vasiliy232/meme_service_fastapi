__all__ = (
    'create_file',
    'delete_file',
    'get_file_by_name',
)

from sqlalchemy.orm import Session
from models import File
from schemas import FileCreate
from sqlalchemy.exc import DatabaseError
import logging

log = logging.getLogger(__name__)

def get_file_by_name(db: Session, filename: str):
    return db.query(File).filter(File.filename == filename).first()

def create_file(db: Session, file: FileCreate):
    db_file = File(filename=file.filename, s3_url=file.s3_url)
    db.add(db_file)
    try:
        db.commit()
        db.refresh(db_file)
        return db_file
    except DatabaseError:
        log.exception('Could not add file %s', file)
        db.rollback()

def delete_file(db: Session, file: File):
    db.delete(file)
    db.commit()
