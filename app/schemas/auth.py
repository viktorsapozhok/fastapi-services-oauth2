from app.schemas.base import BaseSchema


class CreateUserSchema(BaseSchema):
    name: str
    email: str
    password: str


class UserSchema(BaseSchema):
    name: str
    email: str
    hashed_password: str | None = None


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str
