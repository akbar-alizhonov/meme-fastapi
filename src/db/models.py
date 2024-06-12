from sqlalchemy import Column, Integer, String
from db.database import Base


class Meme(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    image = Column(String)
