from fastapi import FastAPI
from . import models
from .config import engine
from .routers import post, users


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
