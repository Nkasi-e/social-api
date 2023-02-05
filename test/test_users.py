import pytest
from app import schemas
from jose import jwt
from app.oauth2 import JWT_ALGORITHM, JWT_SECRET_KEY


def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == "Welcome to Social Hub"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        '/users/', json={"email": "test@gmail.com", "password": "Testpassword1"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        '/login', data={"username": test_user['email'], "password": test_user['password']})  # we used data because we didn't use a json format but a form-data from the body
    login_response = schemas.Token(**res.json())
    payload = jwt.decode(login_response.access_token,
                         JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == 'Bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'Testpassword1', 403),
    ('test@gmail.com', 'wrongPassword', 403),
    ('wrongemail@gmail.com', 'wrongPassword', 403),
    (None, 'Testpassword1', 422),
    ('test@gmail.com', None, 422)
])
def test_failed_login(client, test_user, email, password, status_code):
    res = client.post(
        '/login', data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials'
