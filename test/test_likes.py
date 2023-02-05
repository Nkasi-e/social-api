import pytest
from app import models


@pytest.fixture
def test_like(test_post, database, test_user):
    new_like = models.Like(post_id=test_post[3].id, user_id=test_user['id'])
    database.add(new_like)
    database.commit()
    return new_like


def test_like_on_post(authorized_client, test_post):
    res = authorized_client.post(
        f'/likes/', json={"post_id": test_post[0].id, "dir": 1})
    assert res.status_code == 201


def test_unable_to_like_post_twice(authorized_client, test_post, test_like):
    res = authorized_client.post(
        f'/likes/', json={"post_id": test_post[3].id, "dir": 1})
    assert res.status_code == 409


def test_unlike_post(authorized_client, test_post, test_like):
    res = authorized_client.post(
        f'/likes/', json={"post_id": test_post[3].id, "dir": 0})
    assert res.status_code == 201


def test_unlike_post_not_exist(authorized_client, test_post):
    res = authorized_client.post(
        f'/likes/', json={"post_id": test_post[3].id, "dir": 0})
    assert res.status_code == 404


def test_unlike_post_that_does_not_exist(authorized_client, test_post):
    res = authorized_client.post(
        f'/likes/', json={"post_id": 10, "dir": 1})
    assert res.status_code == 404


def test_unauthenticated_user_like_on_post(client, test_post):
    res = client.post(
        f'/likes/', json={"post_id": test_post[0].id, "dir": 1})
    assert res.status_code == 401
