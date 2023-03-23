# Password hash function
from passlib.context import CryptContext  # for password hashing

# hashing algorithm we wanna use which is bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hashing function
def password_hash(password: str):
    return pwd_context.hash(password)


# Verifying password hash


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
