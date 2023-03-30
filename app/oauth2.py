import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from datetime import datetime, timedelta
from .config import get_db
from .models import User
from sqlalchemy.orm import Session

from dotenv import load_dotenv

from .schemas import TokenData

load_dotenv()


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
EXPIRES_IN = float(os.environ.get("EXPIRES_IN"))


# creating token fn
def create_access_token(data: dict):
    to_encode = data.copy()  # making a copy of the data

    expires = datetime.utcnow() + timedelta(days=EXPIRES_IN)
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):  # Verifying token fn
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWSError:
        raise credentials_exception
    return token_data


# Authentication fn
def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthorized failed. Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user
