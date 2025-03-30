from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):

    db_async_connection_str : str
    model_config = SettingsConfigDict(env_file="../.env")
    
settings = Settings()    