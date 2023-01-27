import os
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import time

load_dotenv()

# working_directory = os.getcwd()
# env = os.path.join(working_directory, '.env')
# # loading evn
# if os.path.exists(env):
#     load_dotenv(env)
#     print('env loaded successfully')
# else:
#     print('could not find environment')

app = FastAPI()


class Post(BaseModel):
    id: Optional[int]
    title: str
    content: str
    published: Optional[bool] = True


class UpdatePost(BaseModel):
    id: Optional[int]
    title: Optional[str]
    content: Optional[str]
    published: Optional[bool] = True


while True:
    try:
        conn = psycopg2.connect(host=os.getenv('DB_HOST'), database=os.environ.get(
            'USER_DB'), user='postgres', password=os.environ.get('DB_PASSWORD'), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection established')
        break
    except Exception as error:
        print(f'Connection to database failed {error}')
        time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get('/posts')
async def get_posts():
    cursor.execute('''SELECT * FROM posts''')
    db_post = cursor.fetchall()
    return {"My Posts": db_post, "total": len(db_post)}


@app.get('/posts/latest')
async def get_latest_posts():
    cursor.execute('''SELECT * FROM posts''')
    db_post = cursor.fetchall()
    post = db_post[len(db_post)-1]
    return {"latest Post": post}


@app.post('/posts', status_code=201)
async def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get('/posts/{id}')
async def get_posts(id: int):
    cursor.execute('''SELECT * FROM posts WHERE id = %s ''', (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found'
        )
    return {"Post detail": post}


@app.delete('/posts/{id}', status_code=204)
async def delete_post(id: int):
    cursor.execute(
        '''DELETE FROM posts WHERE id = %s RETURNING * ''', (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    return


@app.put('/posts/{id}')
async def update_post(id: int, post: UpdatePost):
    cursor.execute('''UPDATE posts SET content = %s, published = %s WHERE id = %s RETURNING *''',
                   (post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    return {"data": updated_post}


# @app.patch('/posts/{id}')
# async def update_post(id: int, post: UpdatePost):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f'Post with id {id} not found')
#     post_dict = post.dict()
#     post_dict['id'] = id
#     posts[index] = post_dict
#     return {"message": f'Post with id {id} successfully updated', "data": post_dict}
