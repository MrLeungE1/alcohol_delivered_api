from typing import Optional, List
from pydantic import BaseModel, Field

class ProductImageItem(BaseModel):
    image_url: str = Field(..., description="图片URL")
    image_type: int = Field(1, ge=1, le=2, description="1=轮播图,2=详情图")
    sort: int = Field(0, ge=0, description="排序")

class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    image_type: int
    sort: int
    product_id: int

    model_config = {"from_attributes": True}

class CreateProductRequest(BaseModel):
    cate_id: int = Field(..., gt=0, description="分类ID")
    product_name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    price: float = Field(..., gt=0, description="售价")
    market_price: Optional[float] = Field(None, description="原价/划线价")
    thumb: Optional[str] = Field(None, description="商品缩略图")
    # detail_img: Optional[str] = Field(None, description="详情图片(JSON)")
    images: Optional[List[ProductImageItem]] = Field(None, description="商品图片列表（轮播图、详情图）")
    stock: int = Field(0, ge=0, description="库存")
    is_hot: int = Field(0, ge=0, le=1, description="1=热销")
    is_special: int = Field(0, ge=0, le=1, description="1=特价")
    desc: Optional[str] = Field(None, description="商品描述")
    status: int = Field(1, ge=0, le=1, description="1=上架 0=下架")

class SearchProductRequest(BaseModel):
    product_name: Optional[str] = None
    cate_id: Optional[int] = None
    status: Optional[int] = None
    stock: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    cate_id: int
    product_name: str
    price: float
    market_price: Optional[float] = None
    thumb: Optional[str] = None
    # detail_img: Optional[str] = None
    images: Optional[List[ProductImageResponse]] = []
    stock: int
    is_hot: int
    is_special: int
    desc: Optional[str] = None
    status: int

    model_config = {"from_attributes": True}

class EditProductRequest(BaseModel):
    id: int
    cate_id: Optional[int] = None
    product_name: Optional[str] = None
    price: Optional[float] = None
    market_price: Optional[float] = None
    thumb: Optional[str] = None
    # detail_img: Optional[str] = None
    images: Optional[List[ProductImageItem]] = None
    stock: Optional[int] = None
    is_hot: Optional[int] = None
    is_special: Optional[int] = None
    desc: Optional[str] = None
    status: Optional[int] = None

    model_config = {"from_attributes": True}