from pydantic import BaseSettings

from app.const import (
    AUTH_OFF,
    AUTH_ON,
    ENV_DEV,
)


class Settings(BaseSettings):
    env: str = ENV_DEV
    auth: str = AUTH_ON

    @property
    def auth_disabled(self) -> bool:
        return self.auth == AUTH_OFF


settings = Settings()
