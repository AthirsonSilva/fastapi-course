from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_PASSWORD: str = "%40Potter77"
    DATABASE_NAME: str = "fastapi"
    DATABASE_USERNAME: str = "postgres"
    SECRET_KEY: str = "b84eb41558f3cf0f08fae0f43d462b7e4a0a22a46f409fa314b26bc01ea32b85"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = "./.env"


settings = Settings()
