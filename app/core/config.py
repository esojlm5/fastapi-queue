from uuid import UUID
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    SUPABASE_URL: str
    SUPABASE_KEY: str
    API_TOKEN: UUID

    # This configuration tells Pydantic to load variables from a .env file
    # if it exists, which is perfect for local development.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
