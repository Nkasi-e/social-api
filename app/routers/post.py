from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import Post
from ..config import get_db
from ..schemas import CreatePost, PostOut


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts


@router.post('/', status_code=201, response_model=PostOut)
async def create_post(post: CreatePost, db: Session = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=PostOut)
async def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found'
        )
    return post


@router.delete('/{id}', status_code=204)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    post.delete(synchronize_session=False)
    db.commit()
    return


@router.put('/{id}', response_model=PostOut)
async def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} does not exists'
        )
    update_data = updated_post.dict(exclude_unset=True)
    post_query.filter(Post.id == id).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
