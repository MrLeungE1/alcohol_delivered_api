from app.db.base import Base
from sqlalchemy import Column, Integer, String

class ProductCategory(Base):
    __tablename__ = "product_category"

    id = Column(Integer, primary_key=True, index=True, comment="分类ID")
    cate_name = Column(String(255), nullable=False, comment="分类名称")
    sort = Column(Integer, default=0, comment="排序")
    status = Column(Integer, default=1, comment="状态 1:正常 2:禁用")
