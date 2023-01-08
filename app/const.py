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

# Movies service constants
MOVIES_TAGS: Final[List[str | Enum] | None] = ["Movies"]
MOVIES_URL: Final = "movies"
MOVIES_URL_NEW: Final = "new"
MOVIES_URL_GENRE: Final = "genre"
