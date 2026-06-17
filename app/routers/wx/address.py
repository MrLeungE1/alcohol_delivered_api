from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.wx.address import UserAddressService
from app.schemas.wx.address import AddressCreateRequest, AddressCreateResponse, EditAddressRequest

router = APIRouter(prefix="/address", tags=["收货地址管理"])
address_services = UserAddressService()
# 收货地址的增删改查
# 新增地址
# 删除地址
# 修改地址
# 查询地址列表
# 设置默认地址

@router.get("/list", summary="查询地址列表")
def get_address_list(user_id: int, db: Session = Depends(get_db)):
    # 获取用户的地址列表
    return address_services.getAddressList(db, user_id=user_id)
   
@router.post('/add',response_model=list[AddressCreateResponse], summary="新增地址")
def add_address(request: AddressCreateRequest, db: Session = Depends(get_db)):
    # 新增地址
    return address_services.createAddress(db, request)

@router.post("/edit", response_model=AddressCreateResponse, summary="修改地址")
def edit_address(request: EditAddressRequest, db: Session = Depends(get_db)):
    # 修改地址
    return address_services.updateAddress(db, request)

@router.delete("/{id}", summary="删除地址")
def delete_address(id: int, db: Session = Depends(get_db)):
   return address_services.deleteAddress(db, id)