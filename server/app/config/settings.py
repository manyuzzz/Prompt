from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AI Placement Preparation Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    PORT: int = 5000

    MONGODB_URI: str = "mongodb://localhost:27017/placement-ai"
    DATABASE_NAME: str = "placement-ai"

    JWT_SECRET: str = "super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080  # 7 days

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    GEMINI_API_KEY: Optional[str] = None
    AI_PROVIDER: str = "mock"  # 'openai', 'gemini', 'mock'

    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    UPLOAD_DIR: str = "uploads"

    CODE_RUNNER_URL: str = "http://localhost:6000"
    CLIENT_URL: str = "http://localhost:5173"

    RATE_LIMIT_WINDOW: int = 15
    RATE_LIMIT_MAX: int = 100

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
