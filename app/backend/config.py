from pydantic import BaseSettings
from pydantic import PostgresDsn

from app.const import ENV_PREFIX


class Settings(BaseSettings):
    """API configuration parameters.

    Automatically read modifications to the configuration parameters
    from environment variables.

    Each environment variable should have prefix given by ``ÈNV_PREFIX``
    constant. Constants are specified via :mod:`~app.const`.

    Attributes:
        dsn:
            Postgres connection string.
        token_key:
            Random secret key used to sign JWT tokens.
    """

    dsn: PostgresDsn
    token_key: str

    class Config:
        env_prefix = ENV_PREFIX


settings = Settings()
