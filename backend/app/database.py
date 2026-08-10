from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine

from app.config import get_settings


settings = get_settings()


if settings.turso_database_url and settings.turso_auth_token:
    # Production: Turso
    turso_url = settings.turso_database_url

    if turso_url.startswith("libsql://"):
        turso_url = turso_url.replace(
            "libsql://",
            "sqlite+libsql://",
            1
        )

    engine = create_engine(
        turso_url,
        connect_args={
            "auth_token": settings.turso_auth_token
        },
    )

else:
    # Local development: SQLite
    db_path = settings.database_url.replace(
        "sqlite:///",
        "",
        1
    )

    if not db_path.startswith(":memory:"):
        Path(db_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

    engine = create_engine(
        settings.database_url,
        connect_args={
            "check_same_thread": False
        },
    )


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session