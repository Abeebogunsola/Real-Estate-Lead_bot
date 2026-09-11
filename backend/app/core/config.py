"""Application configuration loaded from environment variables."""

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
    cors_origins: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080"

    database_url: str = "mysql+pymysql://relb:relbsecret@localhost:3306/real_estate_leads"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    n8n_webhook_url: str = "http://n8n:5678/webhook/lead-process-message"
    n8n_webhook_secret: str = "change-me-n8n-secret"

    ai_api_key: str = ""
    ai_model: str = "gpt-4o-mini"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
