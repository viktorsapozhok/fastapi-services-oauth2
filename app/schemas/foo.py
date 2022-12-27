from pydantic import BaseModel


class ItemSchema(BaseModel):
    item_id: int
    description: str
    public: bool

    class Config:
        orm_mode = True
