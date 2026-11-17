from __future__ import annotations

import re
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_CONNECTION_URL = re.compile(r"(?i)\bpostgres(?:ql)?(?:\+\w+)?://[^\s'\"<>]+")


def redact_connection_urls(message: str) -> str:
    return _CONNECTION_URL.sub("[redacted connection URL]", message)


class Settings(BaseSettings):
    """Typed configuration for the ORDO storage package."""

    database_url: str = Field(
        alias="DATABASE_URL",
    )
    database_url_unpooled: str = Field(
        alias="DATABASE_URL_UNPOOLED",
    )

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgresql://") and "+asyncpg" not in value:
            value = value.replace("postgresql://", "postgresql+asyncpg://", 1)
            value = value.replace("sslmode=require", "ssl=require")
            value = value.replace("&channel_binding=require", "")
            value = value.replace("?ssl=require&ssl=require", "?ssl=require")
        return value

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()
