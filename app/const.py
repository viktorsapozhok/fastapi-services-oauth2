from enum import Enum
from typing import Final
from typing import List

# Application name
APP_NAME: Final = "app"

# Environment variables prefix
ENV_PREFIX: Final = "api_"

# Turn on/off authentication
AUTH_ON: Final = "on"
AUTH_OFF: Final = "off"

# User schema in case of no authentication
DEFAULT_USER_ID: Final = -1
DEFAULT_USER_EMAIL: Final = "email"

# Open API parameters
OPEN_API_TITLE: Final = "API Hub"
OPEN_API_DESCRIPTION: Final = "Demo API built with FastAPI over Postgres database."

# Database schema name
DATABASE_SCHEMA: Final = "dbt_mmapi"

# Authentication service constants
AUTH_TAGS: Final[List[str | Enum] | None] = ["Authentication"]
AUTH_URL: Final = "token"  # authentication

TOKEN_TYPE: Final = "bearer"
TOKEN_EXPIRE_MINUTES: Final = 60

# Algorithm used to sign the JWT tokens
TOKEN_ALGORITHM: Final = "HS256"

# Foo service constants
FOO_TAGS: Final[List[str | Enum] | None] = ["Foo"]
FOO_URL: Final = "foo"  # Foo service
FOO_URL_ITEM: Final = "item"
FOO_URL_ITEMS: Final = "items"
FOO_URL_PUBLIC_ITEMS: Final = "public_items"
