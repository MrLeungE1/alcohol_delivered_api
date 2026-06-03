from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class SysUser(Base):
    __tablename__ = "sys_user"

    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    openid = Column(String(255), nullable=False, index=True, comment="微信小程序唯一标识")
    nickname = Column(String(255), nullable=False, comment="昵称")
    avatar = Column(String(255), nullable=True, comment="头像")
    phone = Column(String(255), nullable=True, comment="手机号")
    default_addr_id = Column(Integer, ForeignKey("user_address.id"), nullable=True, comment="默认地址ID")
    create_time = Column(DateTime, default=func.now(), comment="创建时间")

    # 🔥 修复：指定外键，解决歧义
    addresses = relationship(
        "UserAddress",
        foreign_keys="UserAddress.user_id",  # 关键
        back_populates="user"
    )
    # 默认地址单独关联
    default_address = relationship("UserAddress", foreign_keys=[default_addr_id])