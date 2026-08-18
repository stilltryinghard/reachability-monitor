from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    mongo_url: str = "mongodb://localhost:27017"
    db_name: str = "reachability"
    
    
settings = Settings()