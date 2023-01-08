from pydantic import BaseModel


class MovieSchema(BaseModel):
    movie_id: int
    title: str
    released: int
    rating: float

    class Config:
        orm_mode = True
