from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
)

from app.models.base import (
    BaseModel,
    TableValuedMixin,
)


class MovieModel(BaseModel):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String)
    released = Column(Integer)
    rating = Column(Float)


class GenreMovieModel(TableValuedMixin, BaseModel):
    __tablename__ = "genre_movies"

    movie_id = Column(Integer, primary_key=True)
    genre = Column(String, primary_key=True)
    title = Column(String)
    released = Column(Integer)
    rating = Column(Float)
