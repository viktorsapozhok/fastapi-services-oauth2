import os
from typing import Iterator

from omegaconf import DictConfig
from omegaconf import OmegaConf
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.backend.config import settings
from app.const import CONF_FILE, DATABASE_SCHEMA

_PATH_CONF = os.path.dirname(os.path.abspath(__file__))


def create_factory(env: str) -> sessionmaker:
    """Create session factory which generates database sessions when called

    Args:
        env:
            Environment tag (dev/prod). Used to identify which database to connect.

    Returns:
        SQLAlchemy session factory.
    """

    conn_args = get_conn_args(env)

    url = URL.create(
        drivername="postgresql",
        username=get_env(conn_args.user),
        password=get_env(conn_args.password),
        host=get_env(conn_args.host),
        port=int(get_env(conn_args.port)),
        database=get_env(conn_args.dbname),
    )

    engine = create_engine(url)

    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_conn_args(env: str) -> DictConfig:
    """Parse config file and return database connection parameters."""

    config = DictConfig(OmegaConf.load(os.path.join(_PATH_CONF, CONF_FILE)))

    return config.database[env]


def get_env(env_name: str) -> str:
    value = os.getenv(env_name)
    if value is None:
        raise KeyError(f"Environment variable {env_name} is missing")
    return value


# create session factory to generate new database sessions
SessionFactory = create_factory(settings.env)

# declarative base class used to construct mappings
Base = declarative_base(metadata=MetaData(schema=DATABASE_SCHEMA))


def create_session() -> Iterator[sessionmaker]:
    """Create new database session.

    Yields:
        The database session.
    """

    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()
