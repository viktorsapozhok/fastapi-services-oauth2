from typing import List

from app.models.foo import ItemModel
from app.schemas.foo import ItemSchema
from app.services.base import AppCRUD, AppService


class FooService(AppService):
    def get_item(self, item_id: int) -> ItemSchema:
        return FooCRUD(self.db).get_item(item_id)

    def get_items(self) -> List[ItemSchema]:
        return FooCRUD(self.db).get_items()

    def get_public_items(self) -> List[ItemSchema]:
        return FooCRUD(self.db).get_public_items()


class FooCRUD(AppCRUD):
    def get_item(self, item_id: int) -> ItemSchema:
        return ItemSchema.from_orm(self.query(ItemModel, item_id=item_id).first())

    def get_items(self) -> List[ItemSchema]:
        return [ItemSchema.from_orm(obj) for obj in self.query(ItemModel).all()]

    def get_public_items(self) -> List[ItemSchema]:
        items = self.query(ItemModel, public=True).all()

        return [ItemSchema.from_orm(obj) for obj in items]
