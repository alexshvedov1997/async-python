import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_NAME: str = Field('short_url', env='PROJECT_NAME')
    DB_USER: str = Field(env="DB_USER")
    DB_NAME: str = Field(env="DB_NAME")
    DB_HOST: str = Field(env="DB_HOST")
    DB_PORT: str = Field(env="DB_PORT")
    DB_PASSWORD: str = Field(env="DB_PASSWORD")
    SECRET_KEY: str = Field(env="SECRET_KEY")
    SAULT: str = Field(env="SAULT")
    BUCKET_NAME: str = Field(env="BUCKET_NAME")
    AWS_KEY_ID: str = Field(env="AWS_KEY_ID")
    AWS_SECRET_ACCESS_ID: str = Field(env="AWS_SECRET_ACCESS_ID")
    AWS_REGION_NAME: str = Field(env="AWS_REGION_NAME")
    REDIS_HOST: str = Field(env="REDIS_HOST")
    REDIS_PORT: str = Field(env="REDIS_PORT")

    class Config:
        env_file = '.env'


settings = Settings()
