import os
from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///./citas_criterios.sqlite3"
)

# Compatibilidad con PostgreSQL de Render
if database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

connect_args = (
    {"check_same_thread": False}
    if database_url.startswith("sqlite")
    else {}
)

engine = create_engine(
    database_url,
    echo=False,
    connect_args=connect_args
)


@asynccontextmanager
async def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)

    try:
        from load_dataset import cargar_dataset
        cargar_dataset()
    except Exception as e:
        print(f"Error cargando dataset: {e}")

    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]