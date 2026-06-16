from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.user_cart import UserCart

from app.schemas.wx.cart import AddCartRequest, ChangeCartNumRequest

class CartService:
    def addProductToCart(self, db: Session, request: AddCartRequest):
        # 加入购物车的逻辑
        """
        判断商品是否存在、判断商品库存是否足够、判断表中用户是否已存在该商品的购物车：如果有的话增加数量，否则新增购物车
        """
        now_user = db.query(UserCart).filter(UserCart.user_id == request.user_id, UserCart.product_id == request.product_id).first()
        if now_user:
            now_user.num += request.num
            now_user.total_price += request.total_price
            db.commit()
            return now_user
        product = db.query(Product).filter(Product.id == request.product_id).first()  #可以看到商品的时候证明商品库存还是有的，所以这里不用判断商品的库存问题
        if product is None:
            return {"message": "商品不存在"}
        if product.stock < request.num:
            return {"message": "商品库存不足"}
        user_cart = UserCart(
            user_id=request.user_id,
            product_id=request.product_id,
            num=request.num,
            price=request.price,
            total_price=request.total_price,
        )
        db.add(user_cart)
        db.commit()
        return user_cart
    
    def get_cart_list(self, db: Session, user_id: int):
        cart_list = db.query(UserCart).filter(UserCart.user_id == user_id).all()
        if not cart_list:
            return []

        product_ids = [cart.product_id for cart in cart_list]
        product_list = db.query(Product).filter(Product.id.in_(product_ids)).all()
        product_map = {product.id: product for product in product_list}

        result = []
        for cart in cart_list:
            product = product_map.get(cart.product_id)
            result.append({
                "id": cart.id,
                "user_id": cart.user_id,
                "product_id": cart.product_id,
                "num": cart.num,
                "price": cart.price,
                "total_price": cart.total_price,
                "products": product if product else None
            })

        return result

    def change_cart_num(self, db:Session, request: ChangeCartNumRequest):
        # 购物车中的商品
        if request.id:
            cart = db.query(UserCart).filter(UserCart.id == request.id).filter(UserCart.product_id == request.product_id).first()
            if not cart:
                return {"message": "购物车不存在"}
            if request.num == 0:
                # 删除购物车中的商品
                db.query(UserCart).filter(UserCart.id == request.id).filter(UserCart.product_id == request.product_id).delete()
                db.commit()
                return cart
            cart.num = request.num
            cart.total_price = request.total_price
            db.commit()
            return cart
        elif request.product_id:
            cart = db.query(UserCart).filter(UserCart.product_id == request.product_id).first()
            if not cart:
                return {"message": "购物车不存在"}
            if request.num == 0:
                # 删除购物车中的商品
                db.query(UserCart).filter(UserCart.product_id == request.product_id).delete()
                db.commit()
                return cart
            cart.num = request.num
            cart.total_price = request.total_price
            db.commit()
            return cart
        return cart

    def delete_cart(self, db: Session, cart_id: int):
        cart = db.query(UserCart).filter(UserCart.id == cart_id).first()
        if not cart:
            return {"message": "购物车不存在"}
        db.delete(cart)
        db.commit()
        return {"message": "购物车删除成功"}