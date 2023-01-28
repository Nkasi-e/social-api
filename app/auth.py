from fastapi import APIRouter, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .models import User
from .config import get_db
from sqlalchemy.orm import Session
from .schemas import Token
from .utils import verify_password
from .oauth2 import create_access_token


router = APIRouter(
    tags=['Authentication']
)


# Using a fastapi OAuth2PasswordRequestForm class model - request can be made from form-data and not raw JSON on postman
@router.post('/login', response_model=Token)
async def login(user_credencials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == user_credencials.username).first()
    if not user:
        raise HTTPException(
            status_code=403,
            detail='Invalid credentials'
        )
    is_password_correct = verify_password(
        user_credencials.password, user.password)
    if not is_password_correct:
        raise HTTPException(status_code=403, detail='Invalid credentials')
    access_token = create_access_token(
        data={"user_id": user.id, "user_email": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}
