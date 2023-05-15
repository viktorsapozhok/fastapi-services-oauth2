from typing import (
    Any,
    List,
    Sequence,
)

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Executable


class DBSessionMixin:
    """Provides instance of database session."""

    def __init__(self, session: Session) -> None:
        self.db = session


class AppService(DBSessionMixin):
    """Base class for app services."""


class AppCRUD(DBSessionMixin):
    """Base class for CRUD operations over database objects."""

    def get_one(self, select_stmt: Executable) -> Any:
        return self.db.scalar(select_stmt)

    def get_all(self, select_stmt: Executable) -> List[Any]:
        return list(self.db.scalars(select_stmt).all())

    def add_one(self, model: Any) -> None:
        self.db.add(model)

    def add_all(self, models: Sequence[Any]) -> None:
        self.db.add_all(models)
