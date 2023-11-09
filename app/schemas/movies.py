from app.schemas.base import BaseSchema


class MovieSchema(BaseSchema):
    movie_id: int
    title: str
    released: int
    rating: float
