from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.backend.database import create_session
from app.const import (
    FOO_URL,
    FOO_URL_ITEM,
    FOO_URL_ITEMS,
    FOO_URL_PUBLIC_ITEMS,
    FOO_TAGS,
)
from app.schemas.auth import UserSchema
from app.schemas.foo import ItemSchema
from app.services.auth import get_current_user
from app.services.foo import FooService

router = APIRouter(prefix="/" + FOO_URL, tags=FOO_TAGS)


@router.get("/" + FOO_URL_ITEM, response_model=ItemSchema)
async def get_item(
    item_id: int,
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> ItemSchema:
    return FooService(session).get_item(item_id)


@router.get("/" + FOO_URL_ITEMS, response_model=List[ItemSchema])
async def get_items(
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> List[ItemSchema]:
    return FooService(session).get_items()


@router.get("/" + FOO_URL_PUBLIC_ITEMS, response_model=List[ItemSchema])
async def get_public_items(
    user: UserSchema = Depends(get_current_user),
    session: Session = Depends(create_session),
) -> List[ItemSchema]:
    return FooService(session).get_public_items()
