from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    QWEN_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
