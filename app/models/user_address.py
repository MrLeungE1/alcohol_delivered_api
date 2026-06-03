from app.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class UserAddress(Base):
    __tablename__ = "user_address"

    id = Column(Integer, primary_key=True, index=True, comment="用户地址ID")    
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=True, comment="用户ID")
    consignee = Column(String(255), nullable=True, comment="收货人姓名")
    phone = Column(String(255), nullable=True, comment="收货人手机号")
    address = Column(String(255), nullable=True, comment="省市县")
    detail_addr = Column(String(255), nullable=True, comment="详细地址")
    lonlat = Column(String(255), nullable=False, comment="经纬度")
    is_default = Column(Integer, nullable=True, default=0, comment="是否默认地址 1:是 0:否")

    # 🔥 修复：对应 back_populates
    user = relationship(
        "SysUser",
        foreign_keys=[user_id],
        back_populates="addresses"
    )