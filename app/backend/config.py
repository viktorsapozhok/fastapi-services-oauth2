from pydantic import BaseSettings
from pydantic import PostgresDsn

from app.const import AUTH_OFF, AUTH_ON


class Settings(BaseSettings):
    dsn: PostgresDsn
    token_key: str
    auth: str = AUTH_ON

    class Config:
        env_prefix = "api_"

    @property
    def auth_disabled(self) -> bool:
        return self.auth == AUTH_OFF


settings = Settings()
