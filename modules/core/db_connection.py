from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@localhost:5433/ecommerce_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session