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

    def query(
        self, model: Type[BaseModel], *filter_args: Any, **filter_kwargs
    ) -> Query:
        """Helper function used to construct basic SELECT statements.

        If ``model`` has mapping with table function then ``filter_args``
        represent function input parameters which should be passed in the same order
        as they are introduced in Postgres function.

        In case ``model`` has mapping with table or view then ``filter_args``
        represent filtering conditions compatible with SQLAlchemy Query API.

        Examples:

            Construct SELECT query from Postgres function.

            .. code::

                self.query(model, 1, 2, 'AAA')

            Construct SELECT query from table.

            .. code::

                self.query(model, model.x == 1, model.y > 2, model.z.contains('AAA'))
                self.query(model, x == 1, y == 2, z == 'AAA')

        Args:
            model:
                SQLAlchemy mapping object.
            *filter_args:
                Filter conditions if mapping is linked with database table or view.
                Function positional arguments if mapping is linked with table function.
            **filter_kwargs
                Keyword arguments used to construct filters for table (or view)
                mappings.
        """

        if model.is_table_valued():
            query = self.db.execute(select(model.table_valued(*filter_args)))
        else:
            query = self.db.query(model).filter(*filter_args).filter_by(**filter_kwargs)
        return query
