from app.db.base import Base
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import relationship

class UserCart(Base):
    __tablename__ = "user_cart"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, comment="用户ID")
    product_id = Column(Integer, nullable=False, comment="商品ID")
    num = Column(Integer, nullable=False, default=1, comment="数量数量")
    create_time = Column(DateTime, nullable=False, default=func.now(), comment="加入购物车时间")