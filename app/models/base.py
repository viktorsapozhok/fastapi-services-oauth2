from typing import (
    Any,
    Dict,
    List,
)

from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class SQLModel(DeclarativeBase):
    """Base class used for model definitions.

    Provides convenience methods that can be used to convert model
    to the corresponding schema.
    """

    @classmethod
    def fields(cls) -> List[str]:
        """Return list of model field names."""

        mapper = inspect(cls)
        if mapper is None:
            raise TypeError("Cannot inspect model")
        return mapper.attrs.keys()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary."""

        _dict: Dict[str, Any] = dict()
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict
