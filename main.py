from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    id: Optional[int]
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int] = None


class UpdatePost(BaseModel):
    id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool] = True
    rating: Optional[int] = None


posts = [{
    "id": 1,
    "title": "Makaveli",
    "content": "Europwen",
    "published": True,
    "rating": 3

},
    {
    "id": 2,
    "title": "homiw",
    "content": "Example",
    "published": True,
    "rating": 2

},
    {
    "id": 3,
    "title": "hamiede",
    "content": "Example2",
    "published": True,
    "rating": 4

}]


def find_one(id):
    for post in posts:
        if post["id"] == id:
            return post


# this is to iterate over the post and also get the index that's why enumerate is being used
def find_index_post(id):
    for i, post in enumerate(posts):
        if post['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get('/posts')
async def get_posts():
    return {"My Posts": posts, "total": len(posts)}


@app.get('/posts/latest')
async def get_latest_posts():
    post = posts[len(posts)-1]
    return {"latest Post": post}


@app.post('/posts', status_code=201)
async def create_post(post: Post):
    post_dict = post.dict()
    # randrange is for selecting a range of value
    post_dict['id'] = randrange(0, 100)
    posts.append(post_dict)
    return {"data": post_dict}


@app.get('/posts/{id}')
async def get_posts(id: int, response: Response):
    post = find_one(id)
    if post is None:
        # You can also use HTTPException instead for better code experience
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f'Post with id {id} not found'}
    return {"post": post}


@app.delete('/posts/{id}', status_code=204)
async def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    posts.pop(index)
    return


@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    post_dict = post.dict()
    post_dict['id'] = id
    posts[index] = post_dict
    return {"message": f'Post with id {id} successfully updated', "data": post_dict}


@app.patch('/posts/{id}')
async def update_post(id: int, post: UpdatePost):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    post_dict = post.dict()
    post_dict['id'] = id
    posts[index] = post_dict
    return {"message": f'Post with id {id} successfully updated', "data": post_dict}
