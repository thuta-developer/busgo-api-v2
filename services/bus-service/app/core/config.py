"""
Application configuration for Bus Service.

Uses Pydantic Settings — reads from environment variables.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bus Service settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ---------- App ----------
    APP_NAME: str = "bus-service"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=False)

    # ---------- Server ----------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ---------- Database ----------
    POSTGRES_USER: str = "busgo"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    BUS_DB_NAME: str = "bus_db"

    # ---------- Redis ----------
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""

    # ---------- JWT ----------
    JWT_PUBLIC_KEY: str = ""
    JWT_ALGORITHM: str = "RS256"
    JWT_ISSUER: str = "busgo-identity"
    JWT_AUDIENCE: str = "busgo-api"

    # ---------- Service URLs ----------
    IDENTITY_SERVICE_URL: str = "http://identity-service:8000"

    @property
    def database_url(self) -> str:
        """Async PostgreSQL DSN."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.BUS_DB_NAME}"
        )

    @property
    def redis_url(self) -> str:
        """Redis DSN."""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()