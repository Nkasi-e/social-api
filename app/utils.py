# Password hash function
from passlib.context import CryptContext  # for password hashing
# hashing algorithm we wanna use which is bcrypt
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# hashing function
def password_hash(password: str):
    return pwd_context.hash(password)
