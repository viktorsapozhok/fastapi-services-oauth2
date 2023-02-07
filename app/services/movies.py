from typing import List

from app.models.movies import (
    GenreMovieModel,
    MovieModel,
)
from app.schemas.movies import MovieSchema
from app.services.base import (
    AppCRUD,
    AppService,
)


class MovieService(AppService):
    def get_movie(self, movie_id: int) -> MovieSchema:
        """Get movie by ID."""

        return MovieCRUD(self.db).get_movie(movie_id)

    def get_new_movies(self, year: int, rating: float) -> List[MovieSchema]:
        """Get movies released since ``year`` and rated higher than ``rating``."""

        return MovieCRUD(self.db).get_new_movies(year, rating)

    def get_genre_movies(self, genre: str) -> List[MovieSchema]:
        """Get movies of specific genre."""

        return MovieCRUD(self.db).get_genre_movies(genre)


class MovieCRUD(AppCRUD):
    def get_movie(self, movie_id: int) -> MovieSchema:
        """Select movie with ``movie_id``."""

        return MovieSchema.from_orm(self.query(MovieModel, movie_id=movie_id).first())

    def get_new_movies(self, year: int, rating: float) -> List[MovieSchema]:
        """Select movies released since ``year`` and rated higher than ``rating``."""

        query = self.query(
            MovieModel, MovieModel.released >= year, MovieModel.rating >= rating
        )

        return [MovieSchema.from_orm(obj) for obj in query.all()]

    def get_genre_movies(self, genre: str) -> List[MovieSchema]:
        """Select movies of specific genre."""

        query = self.query(GenreMovieModel, genre)

        return [MovieSchema.from_orm(obj) for obj in query.all()]
