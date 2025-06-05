from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345678@localhost:5432/goyos_secrets_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session