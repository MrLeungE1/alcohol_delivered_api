# 读取 .env 配置参数
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str 
    UPLOAD_DIR: str = "uploads"
    class Config:
        env_file = ".env"  # 强制从 .env 加载

settings = Settings()