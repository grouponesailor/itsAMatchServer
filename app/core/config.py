from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ItsAMatch API"
    VERSION: str = "1.0.0"
    
    # MongoDB Settings
    MONGODB_URL: str = "mongodb+srv://groupthreesailor:groupthree@cluster0.44c3nbp.mongodb.net/?retryWrites=true&w=majority"
    DATABASE_NAME: str = "ItsAMatch"
    COLLECTION_NAME: str = "generic"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True

settings = Settings() 