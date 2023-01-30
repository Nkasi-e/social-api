from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from httpx import post
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from ..models import Post, Like, User
from ..config import get_db
from ..schemas import CreatePost, PostOut, PostLike, UserOut
from ..oauth2 import get_current_user


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


# to get all post belonging to users
@router.get('/', response_model=List[PostLike])
async def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), skip: int = 0, limit: int = 10, search: Optional[str] = ""):

    posts = db.query(Post, func.count(Like.post_id).label('likes')).join(
        Like, Post.id == Like.post_id, isouter=True).group_by(Post.id).filter(or_(Post.title.ilike(
            f'%{search}%'), Post.content.ilike(f'%{search}%'))).offset(skip).limit(limit).all()

    return posts

# to get all person posts


@router.get('/myposts', response_model=List[PostOut])
async def get_personal_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0):
    posts = db.query(Post).filter(
        Post.owner_id == current_user.id).offset(skip).limit(limit).all()
    return posts


# creating post to save in the db
@router.post('/', status_code=201, response_model=PostOut)
async def create_post(post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# getting single post by Id from every users post in DB
@router.get('/{id}', response_model=PostLike)
async def get_posts_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    post = db.query(Post, func.count(Like.post_id).label('likes')).join(
        Like, Post.id == Like.post_id, isouter=True).group_by(Post.id).filter(Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found'
        )
    return post


@router.delete('/{id}', status_code=204)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} not found')
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail='User Not Authorized to perform requested action'
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return


@router.put('/{id}', response_model=PostOut)
async def update_post(id: int, updated_post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=404,
            detail=f'Post with id {id} does not exists'
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail='User Not Authorized to perform requested action'
        )
    update_data = updated_post.dict(exclude_unset=True)
    post_query.filter(Post.id == id).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
