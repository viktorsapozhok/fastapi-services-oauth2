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
OPEN_API_DESCRIPTION: Final = """
Demo API built with FastAPI and SQLAlchemy over Postgres database.
"""

# Database schema name
DATABASE_SCHEMA: Final = "api"

# Healthcheck service constants
HEALTH_TAGS: Final[List[str | Enum] | None] = ["Healthcheck"]
HEALTH_URL: Final = "health"
HEALTH_STATUS_URL: Final = "status"
HEALTH_STATUS_ALIVE: Final = "alive"
HEALTH_STATUS_IDLE: Final = "idle"

# Authentication service constants
AUTH_TAGS: Final[List[str | Enum] | None] = ["Authentication"]
AUTH_URL: Final = "token"  # authentication

TOKEN_TYPE: Final = "bearer"
TOKEN_EXPIRE_MINUTES: Final = 60

# Algorithm used to sign the JWT tokens
TOKEN_ALGORITHM: Final = "HS256"
