from pydantic import BaseModel
from typing import Optional
from app.models.user_address import UserAddress

class AddressCreateRequest(BaseModel):
    user_id: int # 用户id
    consignee: str # 收货人姓名
    phone: str # 收货人手机号
    address: str # 省市县
    detail_addr: Optional[str] = None # 详细地址，非必填
    lonlat: str # 经纬度
    is_default: bool = False # 是否是默认地址

class AddressCreateResponse(BaseModel):
    user_id: int # 用户id
    consignee: str # 收货人姓名
    phone: str # 收货人手机号
    address: str # 省市县
    detail_addr: str # 详细地址
    lonlat: str # 经纬度
    is_default: bool = False # 是否是默认地址

class EditAddressRequest(BaseModel):
    id: int # 地址id
    user_id: int # 用户id
    consignee: Optional[str] = None # 收货人姓名，非必填
    phone: Optional[str] = None # 收货人手机号，非必填
    address: Optional[str] = None # 省市县，非必填
    detail_addr: Optional[str] = None # 详细地址，非必填
    lonlat: Optional[str] = None # 经纬度，非必填
    is_default: Optional[bool] = None # 是否是默认地址，非必填