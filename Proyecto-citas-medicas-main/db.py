import os
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends, FastAPI

load_dotenv()

database_url = os.getenv("DATABASE_URL", "sqlite:///./citas_criterios.sqlite3")

connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, echo=False, connect_args=connect_args)


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
