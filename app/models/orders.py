from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, func, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Orders(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(255), nullable=False, comment="订单号")
    user_id = Column(Integer, ForeignKey("sys_user.id"), nullable=False, comment="用户ID")
    address_id = Column(Integer, ForeignKey("user_address.id"), nullable=False, comment="地址ID")
    total_amount = Column(Numeric(10,2), nullable=False, comment="订单金额")
    status = Column(Integer, default=1, comment="1 待配送 2 配送中 3 已完成")
    create_time = Column(DateTime, nullable=False, default=func.now(), comment="订单时间")

    user = relationship("SysUser", backref="orders", lazy="selectin")
    address = relationship("UserAddress", backref="orders", lazy="selectin")
