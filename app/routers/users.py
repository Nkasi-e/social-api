from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..config import get_db
from ..schemas import CreateUser, UserOut
from ..utils import password_hash
from ..models import User


router = APIRouter(prefix="/users", tags=["Users"])


# Get user by email - Controller
def get_user_by_email(db: Session, email: str):
    query = db.query(User).filter(User.email == email).first()
    return query


@router.post("/", status_code=201, response_model=UserOut)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail=f"email already exists")
    # hashing the password
    user.password = password_hash(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserOut)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"user with id {id} not found")
    return user
