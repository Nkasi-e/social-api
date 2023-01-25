from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get('/posts')
async def get_posts():
    return {"data": "This is the list of all the posts in your feed"}


@app.post('/create_post')
async def create_post(payload: dict = Body(...)):
    return {"data": payload}
