from typing import List

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.backend.session import create_session
from app.const import (
    MOVIES_TAGS,
    MOVIES_URL,
    MOVIES_URL_NEW,
)
from app.schemas.auth import UserSchema
from app.schemas.movies import MovieSchema
from app.services.auth import get_current_user
from app.services.movies import MovieService


router = APIRouter(prefix="/" + MOVIES_URL, tags=MOVIES_TAGS)


@router.get("/", response_model=MovieSchema)
async def get_movie(
    movie_id: int,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> MovieSchema:
    """Get movie by ID."""

    return MovieService(session).get_movie(movie_id)


@router.get("/" + MOVIES_URL_NEW, response_model=List[MovieSchema])
async def get_movies(
    year: int,
    rating: float,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> List[MovieSchema]:
    """Get movies by ``year`` and ``rating``."""

    return MovieService(session).get_movies(year, rating)
