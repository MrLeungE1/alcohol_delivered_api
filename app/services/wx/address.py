from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.sys_user import SysUser
from app.models.user_address import UserAddress
from app.schemas.wx.address import AddressCreateRequest, EditAddressRequest

class UserAddressService:
    def createAddress(self, db: Session, request: AddressCreateRequest):
        user_info = db.query(SysUser).filter(SysUser.id == request.user_id).first()
        if not user_info:
            raise HTTPException(status_code=400, detail="用户不存在")
        
        address = UserAddress(
            user_id=request.user_id,
            consignee=request.consignee,
            phone=request.phone,
            address=request.address,
            detail_addr=request.detail_addr or '',
            lonlat=request.lonlat,
            is_default=request.is_default,
        )
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    def getAddressList(self, db: Session, user_id: int):
        address_list = db.query(UserAddress).filter(UserAddress.user_id == user_id).all()
        return address_list

    def updateAddress(self,db: Session, request: EditAddressRequest):
        address = db.query(UserAddress).filter(UserAddress.id == request.id).first()
        if not address:
            raise HTTPException(status_code=400, detail="地址不存在")
        if request.consignee:
            address.consignee = request.consignee
        if request.phone:
            address.phone = request.phone
        if request.address:
            address.address = request.address
        if request.detail_addr:
            address.detail_addr = request.detail_addr or ''
        if request.lonlat:
            address.lonlat = request.lonlat
        if request.is_default is not None:
            address.is_default = request.is_default
        db.commit()
        db.refresh(address)
        return address
    
    def deleteAddress(self, db: Session, id: int):
        address = db.query(UserAddress).filter(UserAddress.id == id).first()
        if not address:
            raise HTTPException(status_code=400, detail="地址不存在")
        db.delete(address)
        db.commit()
        return HTTPException(status_code=204, detail="地址删除成功")