from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Text

class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True, index=True, comment="活动ID")
    activity_name = Column(String(100), nullable=False, comment="活动名称")
    banner = Column(String(255), nullable=False, comment="活动banner")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    status = Column(Integer, default=1, comment="1=正常 0=停用")
    desc = Column(Text, comment="活动描述")

