from enum import Enum
from typing import Final
from typing import List

# Prefix of environment variables specifying config parameters
ENV_PREFIX: Final = "api_"

# Open API parameters
OPEN_API_TITLE: Final = "API Hub"
OPEN_API_DESCRIPTION: Final = "Demo API over Postgres database built with FastAPI."

# Database schema name
DATABASE_SCHEMA: Final = "myapi"

# Authentication service constants
AUTH_TAGS: Final[List[str | Enum] | None] = ["Authentication"]
AUTH_URL: Final = "token"

TOKEN_TYPE: Final = "bearer"
TOKEN_EXPIRE_MINUTES: Final = 60

# Algorithm used to sign the JWT tokens
TOKEN_ALGORITHM: Final = "HS256"

# Foo service constants
FOO_TAGS: Final[List[str | Enum] | None] = ["Foo"]
FOO_URL: Final = "foo"
FOO_URL_ITEM: Final = "item"
FOO_URL_ITEMS: Final = "items"
FOO_URL_PUBLIC_ITEMS: Final = "public_items"
