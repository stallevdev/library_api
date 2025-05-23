from pydantic import BaseSettings


class Settings(BaseSettings):
    TITLE: str
    DESCRIPTION: str
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    HOST: str
    PORT: int

    class Config:
        env_file = ".env"


settings = Settings()
