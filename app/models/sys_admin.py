from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class SysAdmin(Base):
    __tablename__ = "sys_admin"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False, index=True, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码")
    name = Column(String(255), nullable=True, comment="姓名")
    status = Column(Integer, nullable=False, default=1, comment="状态 1:正常 2:禁用")
    create_time = Column(DateTime, default=func.now(), comment="创建时间")
