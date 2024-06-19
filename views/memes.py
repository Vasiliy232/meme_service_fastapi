__all__ = ('memes_router',)

from fastapi import APIRouter, HTTPException, Depends, UploadFile, Request, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from schemas import MemeCreate, Meme, FileBase
from .services import (
    get_memes,
    get_meme,
    create_meme,
    get_meme_by_title,
    delete_meme,
    update_meme,
    delete_file,
)
from models import db_session
from sqlalchemy.orm import Session
from typing import List, Union
import models
from .files import create_or_get_file, s3_client

memes_router = APIRouter()

templates = Jinja2Templates(directory="templates")

async def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()

@memes_router.get("/memes/", response_model=List[Meme], response_class=HTMLResponse)
async def read_memes(request: Request, db: Session = Depends(get_db), page: int = 1, limit: int = 1):
    skip = (page - 1) * limit
    memes = get_memes(db, skip, limit)
    total_memes = len(db.query(models.Meme).all())
    total_pages = total_memes // limit + (total_memes % limit > 0)
    return templates.TemplateResponse(
        "/memes/mainpage.html",
        {"request": request, "memes": memes, "page": page, "total_pages": total_pages, "limit": limit}
    )

@memes_router.get("/memes/{meme_id}/", response_model=Meme, response_class=HTMLResponse)
async def read_meme(request: Request, meme_id: int, db: Session = Depends(get_db)):
    db_meme = get_meme(db, meme_id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    return templates.TemplateResponse("/memes/meme.html", {"request": request, "meme": db_meme})

@memes_router.post("/memes/", response_model=Meme)
async def write_meme(
    meme: MemeCreate = Depends(MemeCreate.as_form),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db_file = await create_or_get_file(file, db)
    meme.file_id = db_file.id

    db_meme = get_meme_by_title(db, meme.title)
    if db_meme != None:        
        return RedirectResponse("/memes/", 400)
    new_meme = create_meme(db, meme)
    return RedirectResponse(f"/memes/{new_meme.id}/", 302)

@memes_router.delete("/memes/{meme_id}/")
async def delete_db_meme(meme_id: int, db: Session = Depends(get_db)):
    db_meme = get_meme(db, meme_id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    if db_meme.file != None:
        s3_client.remove_object("memes", db_meme.file.filename)
        delete_file(db, db_meme.file)
    delete_meme(db, db_meme)

@memes_router.post("/memes/{meme_id}/", response_model=Meme)
async def update_meme_with_post_form(
    meme_id: int,
    meme: MemeCreate = Depends(MemeCreate.as_form),
    file: UploadFile = File(),
    method: Union[str, None] = Form(None),
    db: Session = Depends(get_db),
):
    if method == "PUT":
        return await update_db_meme(meme_id, meme, file, db)
    else:
        raise HTTPException(status_code=405, detail='Method Not Allowed')


@memes_router.put("/memes/{meme_id}/", response_model=Meme)
async def update_db_meme(
    meme_id: int,
    meme: MemeCreate = Depends(MemeCreate.as_form),
    file: UploadFile = File(),
    db: Session = Depends(get_db),
):
    db_meme = get_meme(db, meme_id)
    if not db_meme:
        raise HTTPException(status_code=404, detail="Meme not found")
    if not file.filename:
        file = FileBase(filename=db_meme.file.filename, s3_url=db_meme.file.s3_url)
    
    db_file = await create_or_get_file(file, db)
    meme.file_id = db_file.id
    db_meme.title = meme.title
    db_meme.description = meme.description
    db_meme.file_id = meme.file_id
    update_meme(db, db_meme)
    return RedirectResponse(f"/memes/{meme_id}/", 302)
