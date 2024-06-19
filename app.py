from fastapi import FastAPI, APIRouter
from views import memes_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from models import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

internal_router = APIRouter()

internal_router.include_router(memes_router)
app.include_router(internal_router)

@app.get("/")
async def root():
    return RedirectResponse("/memes/")
