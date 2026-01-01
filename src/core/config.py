from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator
import os

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = int(os.environ.get("PORT", 8000))  # Use Railway's PORT
    API_RELOAD: bool = False

    # CORS Settings
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://gravitymodelo.code7.co.za",
    ]

    # Model Parameters - Defaults
    DEFAULT_DISTANCE_DECAY: float = 2.0
    DEFAULT_TRANSPORT_COST_PER_KM: float = 0.5
    DEFAULT_TRUCK_CAPACITY: int = 30

    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            # Handle both JSON array string and comma-separated
            if v.startswith('['):
                import json
                return json.loads(v)
            return [origin.strip() for origin in v.split(',')]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()