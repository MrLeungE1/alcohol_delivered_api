# 数据库会话创建
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # 检查连接是否有效
    pool_size=10,        # 连接池大小
    max_overflow=20,     # 超出连接池大小的最大连接数
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()