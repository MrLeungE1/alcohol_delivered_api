from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.user_cart import UserCart
from app.models.orders import Orders
from app.models.order_item import OrderItem
from datetime import datetime

from app.schemas.wx.cart import AddCartRequest, ChangeCartNumRequest, SettlementCartRequest

class CartService:
    def addProductToCart(self, db: Session, request: AddCartRequest):
        # 加入购物车的逻辑
        """
        判断商品是否存在、判断商品库存是否足够、判断表中用户是否已存在该商品的购物车：如果有的话增加数量，否则新增购物车
        """
        now_user = db.query(UserCart).filter(UserCart.user_id == request.user_id, UserCart.product_id == request.product_id).first()
        if now_user:
            product = db.query(Product).filter(Product.id == request.product_id).first()
            if product is None:
                raise HTTPException(status_code=404, detail="商品不存在")
            if product.stock < now_user.num + request.num:
                raise HTTPException(status_code=400, detail="商品库存不足")
            now_user.num += request.num
            now_user.total_price += request.total_price
            db.commit()
            db.refresh(now_user)
            return now_user
        product = db.query(Product).filter(Product.id == request.product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="商品不存在")
        if product.stock < request.num:
            raise HTTPException(status_code=400, detail="商品库存不足")
        user_cart = UserCart(
            user_id=request.user_id,
            product_id=request.product_id,
            num=request.num,
            price=request.price,
            total_price=request.total_price,
        )
        db.add(user_cart)
        db.commit()
        db.refresh(user_cart)
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
                raise HTTPException(status_code=404, detail="购物车不存在")
            if request.num == 0:
                db.query(UserCart).filter(UserCart.id == request.id).filter(UserCart.product_id == request.product_id).delete()
                db.commit()
                return cart
            product = db.query(Product).filter(Product.id == request.product_id).first()
            if product is None:
                raise HTTPException(status_code=404, detail="商品不存在")
            if product.stock < request.num:
                raise HTTPException(status_code=400, detail="商品库存不足")
            cart.num = request.num
            cart.total_price = request.total_price
            db.commit()
            db.refresh(cart)
            return cart
        elif request.product_id:
            cart = db.query(UserCart).filter(UserCart.product_id == request.product_id).first()
            if not cart:
                raise HTTPException(status_code=404, detail="购物车不存在")
            if request.num == 0:
                db.query(UserCart).filter(UserCart.product_id == request.product_id).delete()
                db.commit()
                return cart
            product = db.query(Product).filter(Product.id == request.product_id).first()
            if product is None:
                raise HTTPException(status_code=404, detail="商品不存在")
            if product.stock < request.num:
                raise HTTPException(status_code=400, detail="商品库存不足")
            cart.num = request.num
            cart.total_price = request.total_price
            db.commit()
            db.refresh(cart)
            return cart
        raise HTTPException(status_code=400, detail="参数错误")

    def delete_cart(self, db: Session, cart_id: int):
        cart = db.query(UserCart).filter(UserCart.id == cart_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="购物车不存在")
        db.delete(cart)
        db.commit()
        return cart
    
    def settlement_carts(self, db: Session, request: SettlementCartRequest):
        # 这里将购物车列表、配送方式、收货地址id、总金额传过来了。需要先在orders表中插入 用户订单的关联关系。在order_item(订单表)中有订单信息
        # 先创建 订单
        order_no = f"AL{datetime.now().strftime('%Y%m%d%H%M%S')}{request.user_id}"
        order = Orders(
            order_no=order_no,
            user_id=request.user_id,
            delivery_type=request.delivery_type,
            address_id=request.address_id,
            total_amount=request.total_amount,
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        # 再创建 订单商品
        for cart in request.cart_list:
            product = db.query(Product).filter(Product.id == cart.product_id).first()
            if product is None:
                raise HTTPException(status_code=404, detail="商品不存在")
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart.product_id,
                product_name=product.product_name,
                product_img=product.thumb,
                price=cart.price,
                num=cart.num,
                # total_price=cart.total_price,
            )
            db.add(order_item)
        db.commit()
        return order

    
