from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


SQLACHEMY_DATABASE_URL = 'sqlite:///./memes.db'
engine = create_engine(
    SQLACHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
