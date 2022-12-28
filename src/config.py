import os
from functools import lru_cache
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_SCHEMA: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env = os.getenv("ENV_NAME", "test")
        env_file = Path(__file__).parent / f"../.env.{env}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
