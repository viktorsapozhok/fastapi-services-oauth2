from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import SQLModel


class MovieModel(SQLModel):
    __tablename__ = "movies"
    __table_args__ = {"schema": "myapi"}

    movie_id: Mapped[int] = mapped_column("movie_id", primary_key=True)
    title: Mapped[str] = mapped_column("title")
    released: Mapped[int] = mapped_column("released")
    rating: Mapped[float] = mapped_column("rating")
