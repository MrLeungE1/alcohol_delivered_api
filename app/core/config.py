# 读取 .env 配置参数
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    UPLOAD_DIR: str = "uploads"
    JWT_SECRET_KEY: str = "change-this-secret-in-env"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 120

    class Config:
        env_file = ".env"  # 强制从 .env 加载

settings = Settings()