# 小程序端的商品管理
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.admin.product import ProductResponse
from app.services.wx.product import WxProductService

router = APIRouter(prefix="/wx/product", tags=["小程序商品管理"])
wx_product_service = WxProductService()

@router.get("/hot_list", response_model=List[ProductResponse], summary="获取热销商品列表")
def get_product_hot_list(db: Session = Depends(get_db)):
    return wx_product_service.get_hot_product_list(db)
