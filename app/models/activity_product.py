from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class ActivityProduct(Base):
    __tablename__ = "activity_product"
    
    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(Integer, ForeignKey("activity.id"), nullable=False, comment="活动ID")
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, comment="商品ID")

    activity = relationship("Activity", backref="products", lazy="selectin")
    product = relationship("Product", backref="activities", lazy="selectin")

