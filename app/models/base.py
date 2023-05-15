from typing import (
    Any,
    Dict,
)

from sqlalchemy.orm import DeclarativeBase


class SQLModel(DeclarativeBase):
    def to_dict(self) -> Dict[str, Any]:
        _dict: Dict[str, Any] = dict()
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict
