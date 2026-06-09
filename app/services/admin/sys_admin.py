from app.models.sys_admin import SysAdmin
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.admin.sys_admin import SysAdminCreate, SysAdminUpdate, SysAdminLogin, SysAdminLoginResponse

class SysAdminService:
    def create_admin(self, db: Session, request: SysAdminCreate):
        # 检查用户名是否存在
        existing_admin = db.execute(select(SysAdmin).where(SysAdmin.username == request.username)).first()
        if existing_admin:
            raise HTTPException(status_code=400, detail="用户名已存在")

        sys_admin = SysAdmin(
            username=request.username,
            password=request.password,
            name=request.name,
            status=request.status
        )
        try:
            db.add(sys_admin)
            db.commit()
            db.refresh(sys_admin)
        except Exception as e:
            raise HTTPException(status_code=500, detail="创建系统管理员失败")
        return sys_admin

    def update_admin(self, db: Session, request: SysAdminUpdate):
        sys_admin = db.query(SysAdmin).filter(SysAdmin.id == request.id).first()
        if not sys_admin:
            raise HTTPException(status_code=400, detail="系统管理员不存在")
        if request.username:
            sys_admin.username = request.username
        if request.password:
            sys_admin.password = request.password
        if request.name:
            sys_admin.name = request.name
        if request.status is not None:
            sys_admin.status = request.status
        try:
            db.commit()
            db.refresh(sys_admin)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail="更新系统管理员失败")
        return sys_admin
    
    def login_admin(self, db: Session, request: SysAdminLogin):
        sys_admin = db.query(SysAdmin).filter(SysAdmin.username == request.username).first()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',sys_admin)
        if not sys_admin:
            raise HTTPException(status_code=400, detail="系统管理员不存在")
        if sys_admin.password != request.password:
            raise HTTPException(status_code=400, detail="密码错误")
        return SysAdminLoginResponse(token="123456")