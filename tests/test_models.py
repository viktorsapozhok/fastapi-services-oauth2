from pydantic import BaseModel
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import SQLModel


class Model(SQLModel):
    __tablename__ = "test_table"

    x: Mapped[int] = mapped_column("x", primary_key=True)
    y: Mapped[str] = mapped_column("y")


class Schema(BaseModel):
    x: int
    y: str


def test_fields():
    assert Model.fields() == ["x", "y"]


def test_convert():
    model = Model(x=1, y="AAA")
    schema = Schema(**model.to_dict())
    assert schema.x == 1
    assert schema.y == "AAA"
