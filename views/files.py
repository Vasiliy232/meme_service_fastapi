__all__ = (
    's3_client',
    'create_or_get_file',
)

from fastapi import File, UploadFile, Depends, HTTPException
from models import db_session
from minio import Minio
from minio.error import S3Error
from sqlalchemy.orm import Session
from schemas import FileCreate, FileBase
from .services import get_file_by_name, create_file
from io import BytesIO
from typing import Union
import os

MINIO_SERVER_HOST = os.getenv('MINIO_SERVER_HOST', 'localhost')

s3_client = Minio(
    f'{MINIO_SERVER_HOST}:9000',
    access_key='KX1b3P7s9UJpFOjt8qfy',
    secret_key='PmY6oqgcobZ4eNgead2Fda70W8dP0oNPkEPpINpd',
    secure=False,
)

async def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()

async def create_or_get_file(file: Union[UploadFile, FileBase] = File(...), db: Session = Depends(get_db)):
    bucket_name = "memes"
    if type(file) != FileBase:
        found = s3_client.bucket_exists(bucket_name)
        if not found:
            s3_client.make_bucket(bucket_name)

        data = await file.read()
        try:
            s3_client.put_object(bucket_name, file.filename, BytesIO(data), len(data))
        except S3Error:
            raise HTTPException(status_code=500, detail=str(S3Error))
    
    s3_url = s3_client.presigned_get_object(bucket_name, f"{file.filename}")
    upploaded_file = FileCreate(filename=file.filename, s3_url=s3_url)

    db_file = get_file_by_name(db, upploaded_file.filename)
    if db_file == None:
        db_file = create_file(db, upploaded_file)
    return db_file
