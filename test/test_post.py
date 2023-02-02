from typing import List
from app import schemas
import pytest

'''
GET POSTS TEST SUITE
'''


def test_get_all_posts(authorized_client, test_post):
    res = authorized_client.get('/posts/')

    def validate(post):
        return schemas.PostLike(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    # print(posts_list)
    assert len(res.json()) == len(test_post)
    assert res.status_code == 200


def test_unauthorized_user_to_get_posts(client, test_post):
    res = client.get('/posts/')
    assert res.status_code == 401


def test_unauthorized_user_to_get_post_by_id(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401


def test_get_post_by_id_does_not_exit(authorized_client, test_post):
    res = authorized_client.get(f'/posts/80')
    assert res.status_code == 404


def test_get_posts_by_id(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}")
    post = schemas.PostLike(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_post[0].id
    assert post.Post.title == test_post[0].title
    assert post.Post.content == test_post[0].content


'''
CREATE POSTS TEST SUITE
'''


@pytest.mark.parametrize("title, content, published", [
    ("sweet people", "zabalu kune nme meif", True),
    ("second people", "take away the first people", True),
    ("samba people", "mei gobe isha lika giri usu mna", True),
])
def test_create_post(authorized_client, test_user, test_post, title, content, published):
    res = authorized_client.post(
        '/posts/', json={"title": title, "content": content, "published": published})
    created_post = schemas.PostOut(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_post):
    res = authorized_client.post(
        '/posts/', json={"title": "letup", "content": "content lorem"})
    created_post = schemas.PostOut(**res.json())
    assert res.status_code == 201
    assert created_post.title == "letup"
    assert created_post.content == "content lorem"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']


def test_unauthorized_user_to_create_posts(client, test_user, test_post):
    res = client.post(
        '/posts/', json={"title": "letup", "content": "content lorem"})
    assert res.status_code == 401


'''
DELETE POSTS TEST SUITE
'''


def test_unauthorized_user_to_delete_posts(client, test_user, test_post):
    res = client.delete(
        f'/posts/{test_post[0].id}')
    assert res.status_code == 401


def test_delete_post_by_id_does_not_exit(authorized_client, test_post):
    res = authorized_client.delete(f'/posts/80')
    assert res.status_code == 404


def test_delete_post_success(authorized_client, test_post):
    res = authorized_client.delete(f'/posts/{test_post[0].id}')
    assert res.status_code == 204


def test_delete_other_user_posts(authorized_client, test_user, test_post):
    res = authorized_client.delete(f'/posts/{test_post[3].id}')
    assert res.status_code == 401
    assert res.json().get('detail') == 'User Not Authorized to perform requested action'


'''
UPDATE POSTS TEST SUITE
'''


def test_unauthorized_user_to_update_posts(client, test_user, test_post):
    res = client.put(
        f'/posts/{test_post[1].id}', json={"title": "letup", "content": "content lorem"})
    assert res.status_code == 401


def test_update_other_user_posts(authorized_client, test_user, test_post):
    res = authorized_client.put(
        f'/posts/{test_post[3].id}', json={"title": "letup", "content": "content lorem"})
    assert res.status_code == 401
    assert res.json().get('detail') == 'User Not Authorized to perform requested action'


def test_update_post_by_id_does_not_exit(authorized_client, test_post):
    res = authorized_client.put(
        f'/posts/363636', json={"title": "letup", "content": "content lorem"})
    assert res.status_code == 404


def test_update_post_success(authorized_client, test_user, test_post):
    res = authorized_client.put(
        f'/posts/{test_post[1].id}', json={"title": "letup", "content": "content lorem"})
    updated_post = schemas.PostOut(**res.json())
    assert updated_post.title == "letup"
    assert updated_post.content == "content lorem"
    assert res.status_code == 200
