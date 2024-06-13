from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from decouple import config


DB_HOST = config('POSTGRES_HOST')
DB_PORT = config('POSTGRES_PORT')
DB_USER = config('POSTGRES_USER')
DB_PASSWORD = config('POSTGRES_PASSWORD')
DB_NAME = config('POSTGRES_DATABASE')

SQLACHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(
    SQLACHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
