# 商品图片表
from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

class ProductImage(Base):
    __tablename__ = "product_image"
    id = Column(Integer, primary_key=True, index=True, comment="主键")
    product_id = Column(Integer, ForeignKey("product.id"), comment="商品ID") # 外键关联商品表
    image_url = Column(String(500), nullable=False, comment="图片URL")
    image_type = Column(Integer, nullable=False, comment="1=轮播图,2=详情图")
    sort = Column(Integer, nullable=False, comment="排序")

    product = relationship("Product", back_populates="images")
