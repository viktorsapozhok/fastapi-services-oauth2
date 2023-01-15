from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import PostgresDsn

from app.const import ENV_DEV, ENV_PREFIX


class DatabaseConfig(BaseModel):
    """Backend database configuration parameters.

    Attributes:
        prod:
            DSN for production database.
        stage:
            DSN for staging database.
        dev:
            DSN for development database.
        target_schema:
            Name of database target schema.
    """

    prod: PostgresDsn
    stage: PostgresDsn
    dev: PostgresDsn

    target_schema: str


class Config(BaseSettings):
    """API configuration parameters.

    Automatically read modifications to the configuration parameters
    from environment variables and ``.env`` file.

    Each environment variable should have prefix given by ``ÈNV_PREFIX``
    constant. Constants are specified in :mod:`~app.const`.

    Attributes:
        env:
            Backed database environment alias, ``prod``, ``stage``, or ``dev``.
        database:
            Database configuration settings.
            Instance of :class:`app.backend.config.DatabaseConfig`.
        token_key:
            Random secret key used to sign JWT tokens.
    """

    env: str = ENV_DEV

    database: DatabaseConfig
    token_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = ENV_PREFIX
        env_nested_delimiter = "__"
        case_sensitive = False

    @property
    def dsn(self) -> PostgresDsn:
        """Return target database connection string."""

        return getattr(self.database, self.env)


config = Config()
