from fastapi import UploadFile
from pydantic import BaseModel


class SMeme(BaseModel):
    description: str
    image: UploadFile
