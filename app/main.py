from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .config import engine
from .routers import post, users, like
from . import auth


''''
the line of code below is no longer needed because alembic manages our migrations but even if it is not commented out it would not still break anything
'''
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "*",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(like.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
