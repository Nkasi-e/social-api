from fastapi import FastAPI
from . import models
from .config import engine
from .routers import post, users
from . import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router)
app.include_router(post.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
