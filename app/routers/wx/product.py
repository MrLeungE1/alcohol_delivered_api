# 小程序端的商品管理
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.wx.products import ProductResponse, activityListResponse
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

# 获取活动列表  轮播图
@router.get("/activity_list", response_model=List[activityListResponse], summary="获取活动列表")
# 活动列表可以直接在首页展示
def get_product_activity_list(db: Session = Depends(get_db)):
    return wx_product_service.get_activity_list(db)

# 获取活动对应的商品列表
@router.get("/activity_list/{activity_id}", response_model=List[ProductResponse], summary="获取活动对应的商品列表")
def get_product_activity_product_list(activity_id: int, db: Session = Depends(get_db)):
    return wx_product_service.get_activity_product_list(db, activity_id)

# 获取商品详情
@router.get("/detail/{product_id}", response_model=ProductResponse, summary="获取商品详情")
def get_product_detail(product_id: int, db: Session = Depends(get_db)):
    return wx_product_service.get_product_detail(db, product_id)

#  商品分类可以使用管理端的商品分类列表
