from typing import List
from fastapi import FastAPI, HTTPException, Depends
from . import models
from .config import engine, get_db
from sqlalchemy.orm import Session
from .schemas import CreatePost, Post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get('/posts', response_model=List[Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', status_code=201, response_model=Post)
async def create_post(post: CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/posts/{id}', response_model=Post)
async def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found'
        )
    return post


@app.delete('/posts/{id}', status_code=204)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    post.delete(synchronize_session=False)
    db.commit()
    return


@app.put('/posts/{id}', response_model=Post)
async def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} does not exists'
        )
    update_data = updated_post.dict(exclude_unset=True)
    post_query.filter(models.Post.id == id).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
