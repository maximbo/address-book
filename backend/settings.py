from enum import StrEnum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE_PATH_BASE = Path(__file__).resolve().parent.parent


class Environment(StrEnum):
    dev = "dev"
    staging = "staging"
    production = "production"
    testing = "testing"


class Settings(BaseSettings):
    env: Environment = Environment.dev

    redis_dsn: str = "redis://localhost:6379"
    api_root_path: str = ""

    model_config = SettingsConfigDict(
        env_file=(
            ENV_FILE_PATH_BASE / ".env",
            ENV_FILE_PATH_BASE / ".env.stage",
            ENV_FILE_PATH_BASE / ".env.prod",
        ),
        env_file_encoding="utf-8",
    )


settings = Settings()
