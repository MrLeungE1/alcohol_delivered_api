from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

"""
微信端包含了 全部商品(按照类别的)、首页的热销商品、活动
"""

class ProductImageResponse(BaseModel):
    id: int
    image_url: str
    image_type: int
    sort: int
    product_id: int

    model_config = {"from_attributes": True}


class activityListResponse(BaseModel):
    id: int
    activity_name: str
    banner: str
    start_time: datetime
    end_time: datetime
    status: int
    desc: str

    model_config = {"from_attributes": True}


class ProductResponse(BaseModel):
    id: int
    cate_id: int
    product_name: str
    price: float
    market_price: Optional[float] = None
    thumb: Optional[str] = None
    images: Optional[List[ProductImageResponse]] = []
    stock: int
    is_hot: int
    is_special: int
    desc: Optional[str] = None
    status: int

    model_config = {"from_attributes": True}
