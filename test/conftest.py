# this conftest.py is a special test that pytest uses and it allows us to define fixtures in here and any fixture defined in this file will automatically be accessible to any of our tests within this package.. it is package specific, even subpackages will automatically have access to any of these fixtures

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.config import get_db, Base
from app.main import app
import pytest
from alembic import command  # used for testing db
from app.oauth2 import create_access_token
from app import models


from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Dependency
# def override_get_db():

# scope="module"
@pytest.fixture
def database():
    # run our code after our test has finished
    Base.metadata.drop_all(bind=engine)
    # run our code before we return our test
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(database):
    def override_get_db():
        try:
            yield database
        finally:
            database.close()
    app.dependency_overrides[get_db] = override_get_db
    # command.upgrade("head")  # alembic
    yield TestClient(app)
    # command.downgrade("base")  # alembic


@pytest.fixture  # creating data entry for user login
def test_user(client):
    user_data = {
        "email": "test@gmail.com",
        "password": "Testpassword1"
    }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "test123@gmail.com",
        "password": "Testpassword1"
    }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


@pytest.fixture  # creating access_token for registered users for testing
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
# used when we want to test an authorized or authenticated client
def authorized_client(client, token):  # creating authenticated client
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture  # creating post for testing (test post)
def test_post(test_user, database, test_user2):
    post_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id']
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user['id']
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2['id']
        }
    ]

    def create_post_model(post):  # coverting post_data into a list
        return models.Post(**post)
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    database.add_all(posts)
    # database.add_all(
    #     [
    #         models.Post(title="first title", content="first content",
    #                     owner_id=test_user['id']),
    #         models.Post(title="second title",
    #                     content="second content", owner_id=test_user['id']),
    #         models.Post(title="third title", content="third content",
    #                     owner_id=test_user['id']),
    #     ])
    database.commit()
    posts = database.query(models.Post).all()
    return posts
