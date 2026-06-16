# app/models/product.py
from app.db.base import Base
from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, comment="商品ID")
    cate_id = Column(Integer, ForeignKey("product_category.id"), nullable=False, index=True, comment="分类ID")
    product_name = Column(String(100), nullable=False, comment="商品名称")
    price = Column(Numeric(10,2), nullable=False, comment="售价")
    cost_price = Column(Numeric(10,2), comment="进货价")
    market_price = Column(Numeric(10,2), comment="原价/划线价")
    thumb = Column(String(255), comment="商品缩略图")
    # detail_img = Column(String(255), comment="详情图片") # 正常情况下，详情图片不止一张，而且商品还会有自己的轮播图，所以我们从表结构中将这个注释掉，重新创建一张商品图的表与商品进行关联
    stock = Column(Integer, nullable=False, default=0, comment="库存")
    is_hot = Column(Integer, default=0, comment="1=热销商品")
    is_special = Column(Integer, default=0, comment="1=特价商品")
    desc = Column(Text, comment="商品描述")
    status = Column(Integer, default=1, comment="1=上架 0=下架")

    # 关联分类
    category = relationship(
        "ProductCategory",  # 用字符串，避免循环引用
        lazy="selectin"
    )

    images = relationship(
         "ProductImage",
        back_populates="product",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
