from sqlalchemy.orm import Session
from app.models.product import Product

class WxProductService:
    def _visible_product_query(self, db:Session): # 过滤出上架的商品
        return db.query(Product).filter(Product.status == 1)

    def get_hot_product_list(self, db:Session):
        return self._visible_product_query(db).filter(Product.is_hot == 1).all()