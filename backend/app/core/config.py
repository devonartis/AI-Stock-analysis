from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    APP_NAME: str = "Stock Analysis API"
    API_V1_STR: str = "/api/v1"
    OUTPUT_DIR: str = str(Path(__file__).parent.parent / "output")
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

settings = get_settings()
