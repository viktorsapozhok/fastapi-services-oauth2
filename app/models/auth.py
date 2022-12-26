from sqlalchemy import Column
from sqlalchemy import String

from app.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    email = Column(String, primary_key=True)
    name = Column(String)
    hashed_password = Column(String)
