from sqlmodel import Session, SQLModel, create_engine

from career_agent.database.models import JobOfferRecord


DATABASE_URL = "sqlite:///career_agent.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)


def create_database() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)