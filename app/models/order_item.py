from app.db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_item"
    
    id = Column(Integer, primary_key=True, index=True, comment="订单商品ID")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, comment="订单ID")
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, comment="商品ID")
    product_name = Column(String(100), nullable=False, comment="商品名称")
    product_img = Column(String(255), nullable=False, comment="商品图片")
    price = Column(Numeric(10,2), nullable=False, comment="下单时单价")
    num = Column(Integer, nullable=False, default=1, comment="数量数量")
    
    order = relationship("Orders", backref="order_items", lazy="selectin")
    product = relationship("Product", backref="order_items", lazy="selectin")
