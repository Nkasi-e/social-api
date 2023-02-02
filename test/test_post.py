from typing import List
from app import schemas


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
