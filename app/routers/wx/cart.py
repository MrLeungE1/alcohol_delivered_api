from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.wx.cart import AddCartRequest, AddCartResponse, CartListResponse, ChangeCartNumRequest, SettlementCartRequest
from app.services.wx.cart import CartService
from typing import List


router = APIRouter(prefix="/cart", tags=["购物车"])
cart_service = CartService()

# 加入购物车的逻辑
"""
    加入购物车的逻辑是什么？
    在用户点击加入购物车的时候我们是否要判断当前商品是否还有库存?如果商品没有库存了我们是直接提醒客户商品库存不足之后刷新商品列表将库存不足的产品下架？
    如果商品有库存我们是否要判断当前用户是否已经加入购物车了?如果已经加入购物车了我们是否要判断当前用户加入购物车的商品数量是否超过商品的库存数量?如果超过商品的库存数量我们是否要提醒客户商品库存不足之后刷新商品列表将库存不足的产品下架？
"""
@router.post("/add", response_model=AddCartResponse, summary="加入购物车")
def add_cart(request: AddCartRequest, db: Session = Depends(get_db)):
    # 实现加入购物车的逻辑
    return cart_service.addProductToCart(db, request)

# 获取购物车列表
@router.get("/list", response_model=List[CartListResponse], summary="获取购物车列表")
def get_cart_list(user_id: int, db: Session = Depends(get_db)):
    return cart_service.get_cart_list(db, user_id)

# 改变购物车中商品数量
"""
    这里改变购物车的商品数量应该有两种吧：1. 增加 2. 减少(包含删除商品数量为1时再减少为删除)
    还有删除
"""
@router.post('/change', response_model=CartListResponse, summary="改变购物车中商品数量")
def change_cart_num(request: ChangeCartNumRequest, db: Session = Depends(get_db)):
    return cart_service.change_cart_num(db, request)

@router.delete('/{cart_id}', response_model=dict, summary="删除购物车中商品")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    return cart_service.delete_cart(db, cart_id)

@router.post('/settlement', summary="购物车结算创建订单")
def settlement_cart(request: SettlementCartRequest, db: Session = Depends(get_db)):
    return cart_service.settlement_carts(db, request)
