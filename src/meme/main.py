from fastapi import FastAPI
from .router import router as memes_router


app = FastAPI()

app.include_router(memes_router)
