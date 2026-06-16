from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.activity import Activity
from app.models.activity_product import ActivityProduct

class WxProductService:
    def _visible_product_query(self, db:Session): # 过滤出上架的商品
        return db.query(Product).filter(Product.status == 1)

    def get_hot_product_list(self, db:Session):
        return self._visible_product_query(db).filter(Product.is_hot == 1).all()

    def get_activity_list(self, db:Session):
        return db.query(Activity).filter(Activity.status == 1).all()
    
    def get_activity_product_list(self, db:Session, activity_id: int):
        activity_productIds =  db.query(ActivityProduct).filter(ActivityProduct.activity_id == activity_id).all()
        productIds = [item.product_id for item in activity_productIds]
        print(productIds)
        return self._visible_product_query(db).filter(Product.id.in_(productIds)).all()

    def get_product_detail(self, db:Session, product_id: int):
        product_info = db.query(Product).filter(Product.id == product_id).first()
        if not product_info:
            raise HTTPException(status_code=404, detail="商品不存在")
        return product_info
