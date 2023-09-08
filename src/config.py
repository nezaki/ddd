import os
from functools import lru_cache
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_SCHEMA: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @staticmethod
    def assemble_cors_origins(v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / f"../.env.{os.getenv('ENV_NAME', 'test')}",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()  # type: ignore
