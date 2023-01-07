from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from app.backend.config import settings
from app.const import DATABASE_SCHEMA


# create session factory to generate new database sessions
SessionFactory = sessionmaker(
    bind=create_engine(settings.dsn), autocommit=False, autoflush=False
)

# declarative base class used to construct mappings
Base = declarative_base(metadata=MetaData(schema=DATABASE_SCHEMA))


def create_session() -> Iterator[Session]:
    """Create new database session.

    Yields:
        The database session.
    """

    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()
