from typing import Optional
from pydantic import BaseModel, Field


class CreateProductRequest(BaseModel):
    cate_id: int = Field(..., gt=0, description="分类ID")
    product_name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    price: float = Field(..., gt=0, description="售价")
    market_price: Optional[float] = Field(None, description="原价/划线价")
    thumb: Optional[str] = Field(None, description="商品缩略图")
    detail_img: Optional[str] = Field(None, description="详情图片(JSON)")
    stock: int = Field(0, ge=0, description="库存")
    is_hot: int = Field(0, ge=0, le=1, description="1=热销")
    is_special: int = Field(0, ge=0, le=1, description="1=特价")
    desc: Optional[str] = Field(None, description="商品描述")
    status: int = Field(1, ge=0, le=1, description="1=上架 0=下架")

class SearchProductRequest(BaseModel):
    product_name: Optional[str] = Field(None, description="商品名称")
    cate_id: Optional[int] = Field(None, gt=0, description="分类ID")
    status: Optional[int] = Field(None, ge=0, le=1, description="1=上架 0=下架")
    stock: Optional[int] = Field(None, ge=0, description="库存")


class ProductResponse(BaseModel):
    id: int
    cate_id: int
    product_name: str
    price: float
    market_price: Optional[float] = None
    thumb: Optional[str] = None
    detail_img: Optional[str] = None
    stock: int
    is_hot: int
    is_special: int
    desc: Optional[str] = None
    status: int

    model_config = {"from_attributes": True}
