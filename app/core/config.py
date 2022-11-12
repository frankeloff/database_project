from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator

class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    POSTGRES_DSN: Optional[PostgresDsn] = None

    @validator("POSTGRES_DSN", pre=False)
    def assemble_postgres_dsn(
        cls,
        v: Optional[str],
        values: Dict[str, Any],
    ) -> str:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB')}",
        )
    class Config:
        env_file = ".env"

settings = Settings()
