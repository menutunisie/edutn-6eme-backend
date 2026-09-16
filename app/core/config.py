from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application, chargee depuis les variables d'environnement."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"

    # Base de donnees
    database_url: str

    # CORS (liste d'origines separees par des virgules dans le .env)
    cors_origins: str = "http://localhost:3000,http://localhost:8080"

    # Supabase Storage
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_storage_bucket: str = "edutn6-resources"

    # JWT
    jwt_secret_key: str = "changeme"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24h
    refresh_token_expire_days: int = 90

    # Seed du compte administrateur par defaut (cree au demarrage si aucun admin n'existe)
    admin_default_email: str = ""
    admin_default_password: str = ""

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
