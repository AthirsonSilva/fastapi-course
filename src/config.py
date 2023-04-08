from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_PASSWORD: str = "%40Potter77"
    DATABASE_NAME: str = "fastapi"
    DATABASE_USERNAME: str = "postgres"

    class Config:
        env_file = "./.env"


settings = Settings()
