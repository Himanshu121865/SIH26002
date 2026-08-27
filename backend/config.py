import os
from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    APP_NAME: str = "SIH26002 — NER Logistics Platform"
    DEBUG: bool = True

    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/sih26002.db"
    REDIS_URL: str = "redis://localhost:6379"

    VALHALLA_URL: str = "http://localhost:8002"
    TRACCAR_URL: str = "http://localhost:8082"

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    OPENWEATHER_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
