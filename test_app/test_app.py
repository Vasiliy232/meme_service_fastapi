from pytest import fixture
from models import Base, db_session, engine, File
from schemas import MemeCreate, FileCreate
from sqlalchemy.orm import scoped_session, Session as SessionType
from views import create_meme, create_file, get_file_by_name, get_meme_by_title, s3_client
from views.services import get_memes, get_meme, update_meme, delete_meme, delete_file

@fixture
def bd():
    """ Экземпляр базы данных """
    Base.metadata.drop_all(bind=engine)
    bd = Base.metadata.create_all(bind=engine)
    return bd

@fixture
def session():
    """ Экземпляр сессии """
    Session = scoped_session(db_session)
    session: SessionType = Session()
    return session

@fixture
def file_create_schema():
    """ Экземпляр схемы создания модели файла """
    bucket_name = "memes"
    found = s3_client.bucket_exists(bucket_name)
    if found:
        for obj in s3_client.list_objects(bucket_name):
            s3_client.remove_object(bucket_name, obj.object_name)
        s3_client.remove_bucket(bucket_name)
    s3_client.make_bucket(bucket_name)
    s3_client.fput_object('memes', "first-mem.jpg", "./static/images/first-mem.jpg")
    file = FileCreate(filename="first-mem.jpg", s3_url=s3_client.presigned_get_object("memes", "first-mem.jpg"))
    return file

@fixture
def meme_create_schema():
    """ Экземпляр схемы создания модели мема """
    title = "Meme time"
    description = ""
    return MemeCreate(title=title, description=description)

def test_create_file(session, file_create_schema):
    """ Tест создания файла в базе данных """
    file = create_file(session, file_create_schema)
    assert file

def test_get_file_by_name(session, file_create_schema):
    """ Тест запроса файла из базы данных по его имени """
    file = get_file_by_name(session, file_create_schema.filename)
    assert file != None

def test_create_meme(session, meme_create_schema, file_create_schema):
    """ Тест создания мема в базе данных """
    file = get_file_by_name(session, file_create_schema.filename)
    meme_create_schema.file_id = file.id
    meme = create_meme(session, meme_create_schema)
    assert meme != None

def test_get_memes(session, skip=0, limit=100):
    """ Тест запроса списка мемов из базы данных """
    memes = get_memes(session, skip, limit)
    assert memes != None

def test_get_meme(session):
    """ Тест запроса мема из базы данных по его идентификатору """
    first_meme = get_memes(session, limit=1)[0]
    second_meme = get_meme(session, first_meme.id)
    assert first_meme == second_meme

def test_get_meme_by_title(session):
    """ Тест запроса мема из базы данных по его заголовку """
    first_meme = get_memes(session, limit=1)[0]
    second_meme = get_meme_by_title(session, first_meme.title)
    assert first_meme == second_meme

def test_update_meme(session):
    """ Тест обновления данных мема в базе данных """
    meme = get_memes(session, limit=1)[0]
    old_title = meme.title
    new_title = old_title + 'test'
    meme.title = new_title
    update_meme(session, meme)
    meme = get_meme(session, meme.id)
    assert meme.title == new_title
    
def test_delete_meme(session):
    """ Тест удаления мема из базы данных """
    memes = get_memes(session)
    for meme in memes:
        delete_meme(session, meme)
    meme = get_memes(session)
    assert meme == []

def test_delete_file(session, file_create_schema):
    """ Тест удаления файла из базы данных """
    file = get_file_by_name(session, file_create_schema.filename)
    delete_file(session, file)
    file = session.query(File).filter(File.id == file.id).first()
    assert file == None
