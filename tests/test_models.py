from pydantic import BaseModel
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import SQLModel


class Model(SQLModel):
    __tablename__ = "test_table"
    __table_args__ = {"schema": "test_schema"}

    x: Mapped[int] = mapped_column("x", primary_key=True)
    y: Mapped[str] = mapped_column("y")


class Schema(BaseModel):
    x: int
    y: str


def test_schema():
    assert Model.schema() == "test_schema"


def test_table_name():
    assert Model.table_name() == "test_table"


def test_fields():
    assert Model.fields() == ["x", "y"]


def test_dict():
    model = Model(x=1, y="AAA")
    schema = Schema(**model.to_dict())
    assert schema.x == 1
    assert schema.y == "AAA"
