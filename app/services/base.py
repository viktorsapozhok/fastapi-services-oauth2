from typing import Any
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Query, Session

from app.models.base import BaseModel


class DBSessionMixin(object):
    def __init__(self, session: Session):
        self.db = session


class AppService(DBSessionMixin):
    pass


class AppCRUD(DBSessionMixin):
    """Base class for CRUD operations over database objects."""

    def query(self, model: Type[BaseModel], *args: Any, **filter_kwargs: Any) -> Query:
        """Helper function used to construct SELECT statements.

        Positional arguments are used to construct queries from table functions
        and represent function input parameters passed in the same order.

        Keyword arguments are used to construct WHERE clause when querying
        from tables and views.
        """

        if model.is_table_valued():
            query = self.db.execute(select(model.table_valued(*args)))
        else:
            query = self.db.query(model).filter_by(**filter_kwargs)
        return query
