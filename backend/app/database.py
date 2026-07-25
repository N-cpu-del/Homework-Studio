from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings


settings = get_settings()
db_path = settings.database_url.replace("sqlite:///", "", 1)
if not db_path.startswith(":memory:"):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
