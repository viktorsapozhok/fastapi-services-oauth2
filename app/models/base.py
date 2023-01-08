from typing import Any

from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_mixin
from sqlalchemy.sql.selectable import TableValuedAlias

from app.backend.database import Base


@declarative_mixin
class TableValuedMixin:
    """Mixin class used to construct mappings for table valued functions."""

    @classmethod
    def table_valued(cls, *args: Any) -> TableValuedAlias:
        selectable = inspect(cls).selectable
        table_function = getattr(getattr(func, selectable.schema), selectable.name)
        return table_function(*args).table_valued(*selectable.columns.keys())


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def is_table_valued(cls) -> bool:
        return hasattr(cls, "table_valued")
