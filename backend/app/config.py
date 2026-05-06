from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    app_name: str = "iTrip AI Command Center"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./data/app.db"

    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    # AI Provider Configuration
    ai_provider: str = "gemini"  # gemini, openai, anthropic
    ai_model: str = "gemini-1.5-flash"  # default model

    # API Keys
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection_name: str = "itrip_documents"

    # File Upload (optional)
    max_file_size_mb: int = 10
    allowed_file_types: str = "docx,xlsx,pdf"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
