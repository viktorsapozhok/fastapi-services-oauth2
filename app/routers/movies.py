from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.backend.database import create_session
from app.const import (
    MOVIES_URL,
    MOVIES_URL_GENRE,
    MOVIES_URL_NEW,
    MOVIES_TAGS,
)
from app.schemas.auth import UserSchema
from app.schemas.movies import MovieSchema
from app.services.auth import get_current_user
from app.services.movies import MovieService

router = APIRouter(prefix="/" + MOVIES_URL, tags=MOVIES_TAGS)


@router.get("/", response_model=MovieSchema)
async def get_movie(
    movie_id: int,
#    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> MovieSchema:
    """Get movie by ID."""

    return MovieService(session).get_movie(movie_id)


@router.get("/" + MOVIES_URL_NEW, response_model=List[MovieSchema])
async def get_new_movies(
    year: int,
    rating: float,
#    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> List[MovieSchema]:
    """Get movies released since ``year`` and rated higher than ``rating``."""

    return MovieService(session).get_new_movies(year, rating)


@router.get("/" + MOVIES_URL_GENRE, response_model=List[MovieSchema])
async def get_public_items(
    genre: str,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> List[MovieSchema]:
    """Get movies of specific genre."""

    return MovieService(session).get_genre_movies(genre)
