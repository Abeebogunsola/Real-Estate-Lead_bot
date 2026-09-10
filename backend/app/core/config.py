"""
Application configuration loaded from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    app_name: str = "RealEstateLeadBot"
    app_debug: bool = True

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    database_url: str = "postgresql://postgres:postgres@localhost:5432/real_estate_leads"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    n8n_webhook_url: str = ""
    n8n_webhook_secret: str = ""

    ai_api_key: str = ""
    ai_model: str = "gpt-4o-mini"


settings = Settings()
