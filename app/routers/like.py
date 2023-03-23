from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, config, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/", status_code=201)
def like(
    likes: schemas.Like,
    db: Session = Depends(config.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = (
        db.query(models.Post).filter(models.Post.id == likes.post_id).first()
    )  # checking for post
    if post is None:
        raise HTTPException(
            status_code=404, detail=f"Post with id {likes.post_id} does not exist"
        )

        # setting the likes
    like_query = db.query(models.Like).filter(
        models.Like.post_id == likes.post_id, models.Like.user_id == current_user.id
    )
    found_like = like_query.first()
    if likes.dir == 1:
        if found_like:
            raise HTTPException(
                status_code=409, detail=f"user {current_user.id} already liked post"
            )
        new_like = models.Like(post_id=likes.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully liked post"}
    else:
        if not found_like:
            raise HTTPException(status_code=404, detail="Like does not exits")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully unliked post"}
