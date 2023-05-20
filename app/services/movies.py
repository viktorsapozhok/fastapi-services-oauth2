from typing import List

from sqlalchemy import select

from app.models.movies import MovieModel
from app.schemas.movies import MovieSchema
from app.services.base import (
    BaseDataManager,
    BaseService,
)


class MovieService(BaseService):
    def get_movie(self, movie_id: int) -> MovieSchema:
        """Get movie by ID."""

        return MovieDataManager(self.session).get_movie(movie_id)

    def get_movies(self, year: int, rating: float) -> List[MovieSchema]:
        """Select movies with filter by ``year`` and ``rating``."""

        return MovieDataManager(self.session).get_movies(year, rating)


class MovieDataManager(BaseDataManager):
    def get_movie(self, movie_id: int) -> MovieSchema:
        stmt = select(MovieModel).where(MovieModel.movie_id == movie_id)
        model = self.get_one(stmt)

        return MovieSchema(**model.to_dict())

    def get_movies(self, year: int, rating: float) -> List[MovieSchema]:
        schemas: List[MovieSchema] = list()

        stmt = select(MovieModel).where(
            MovieModel.released >= year,
            MovieModel.rating >= rating,
        )

        for model in self.get_all(stmt):
            schemas += [MovieSchema(**model.to_dict())]

        return schemas
