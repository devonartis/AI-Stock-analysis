from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Stock Analysis API"
    
    # Add your other configuration settings here
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
