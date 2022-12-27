from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from app.models.base import BaseModel


class ItemModel(BaseModel):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True)
    description = Column(String)
    public = Column(Boolean, default=False)
