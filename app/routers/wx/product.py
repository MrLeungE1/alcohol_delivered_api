# 小程序端的商品管理
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.admin.product import ProductResponse
from app.services.wx.product import WxProductService

router = APIRouter(prefix="/wx/product", tags=["小程序商品管理"])
wx_product_service = WxProductService()

"""
    1. 首页的活动商品列表
    2. 热销的商品列表
    
"""


@router.get("/hot_list", response_model=List[ProductResponse], summary="获取热销商品列表")
# 热销的商品可以直接在轮播图下方展示
def get_product_hot_list(db: Session = Depends(get_db)):
    return wx_product_service.get_hot_product_list(db)

# 获取活动商品列表
@router.get("/activity_list", response_model=List[ProductResponse], summary="获取活动商品列表")
# 活动商品列表可以直接在首页展示
def get_product_activity_list(db: Session = Depends(get_db)):
    return wx_product_service.get_hot_product_list(db)