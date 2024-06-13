from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from http import HTTPStatus

from db.database import Base
from meme.main import app
from meme.router import get_db
from decouple import config


DB_HOST = config('DB_TEST_HOST')
DB_PORT = config('DB_TEST_PORT')
DB_USER = config('POSTGRES_TEST_USER')
DB_PASSWORD = config('POSTGRES_TEST_PASSWORD')
DB_NAME = config('POSTGRES_TEST_DB')

SQLACHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine = create_engine(
    SQLACHEMY_DATABASE_URL,
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_db() -> None:
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)


def test_add_new_mem():
    meme_id = 1
    params = {'description': 'test description'}
    file_path = 'tests_file/no-image.png'
    upload_file = (
        'no-image.png',
        open(file_path, 'rb'),
        'image/png'
    )
    files = {'image': upload_file}

    response = client.post(
        '/memes',
        params=params,
        files=files,
    )
    data = response.json()
    message = data['message']

    assert response.status_code == HTTPStatus.OK
    assert message == 'Мем успешно добавлен :)'

    response = client.get(f'/memes/{meme_id}')

    assert response.status_code == HTTPStatus.OK
    assert response.headers['description'] == params['description']


def test_read_memes():
    response = client.get('/memes')
    items = response.json()['items']
    assert len(items) == 1


def test_put_meme():
    meme_id = 1
    params = {'description': 'new description'}
    file_path = 'tests_file/no-image.png'
    upload_file = (
        'no-image.png',
        open(file_path, 'rb'),
        'image/png'
    )
    files = {'image': upload_file}

    response = client.put(
        f'/memes/{meme_id}',
        params=params,
        files=files
    )
    message = response.json()['message']

    assert response.status_code == HTTPStatus.OK
    assert message == f'Мем {meme_id} успешно обновлен :)'

    response = client.get(f'/memes/{meme_id}')

    assert response.status_code == HTTPStatus.OK
    assert response.headers['description'] == params['description']


def test_delete_meme():
    meme_id = 1
    response = client.delete(f'/memes/{meme_id}')
    assert response.status_code == HTTPStatus.OK

    response = client.get(f'/memes/{meme_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_db() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)
