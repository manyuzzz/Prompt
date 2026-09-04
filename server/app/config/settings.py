from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AI Placement Preparation Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    PORT: int = 5000

    MONGODB_URI: str = "mongodb://localhost:27017/placement-ai"
    DATABASE_NAME: str = "placement-ai"

    JWT_SECRET: str = "super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_API_KEY: Optional[str] = None
    AI_PROVIDER: str = "mock"

    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    UPLOAD_DIR: str = "uploads"

    CODE_RUNNER_URL: str = "http://localhost:6000"
    CLIENT_URL: str = "http://localhost:5173"

    RATE_LIMIT_WINDOW: int = 15
    RATE_LIMIT_MAX: int = 100

settings = Settings()
