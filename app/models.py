from .config import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    # this relationship maks it to automatically fetch the user data for us
    owner = relationship('User')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
