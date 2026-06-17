# 这里是购物车 的 一些请求、响应的实体
from pydantic import BaseModel
from sqlalchemy import DateTime, func
from app.schemas.wx.products import ProductResponse
from typing import List

# 加入购物车的参数
class AddCartRequest(BaseModel):
    # 这里加入购物车的参数也不对，应该记录用户ID、商品ID、数量、价格、总金额
    user_id: int
    product_id: int
    num: int = 1
    price: float = 0.00
    total_price: float = 0.00

class AddCartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    num: int
    price: float = 0.00
    total_price: float = 0.00

    model_config = {"from_attributes": True}

class CartListResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    num: int
    price: float = 0.00
    total_price: float = 0.00
    products: ProductResponse = None

    model_config = {"from_attributes": True}

class ChangeCartNumRequest(AddCartRequest):
    id: int = None
    

# 购物车结算
class SettlementCartRequest(BaseModel):
    cart_list: List[CartListResponse] = None # 购物车列表
    delivery_type: int = None # 配送方式
    address_id: int = None # 收货地址ID 
    total_amount: float = 0.00 # 总金额
