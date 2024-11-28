from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # app settings
    HOST: str = "localhost"
    PORT: int = 8000

    # db settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "database"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"


settings = Settings()
