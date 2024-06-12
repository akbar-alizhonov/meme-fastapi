from fastapi import FastAPI
from .router import router as memes_router
from fastapi_pagination import add_pagination


app = FastAPI()

app.include_router(memes_router)

add_pagination(app)
