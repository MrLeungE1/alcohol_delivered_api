from app.models.sys_admin import SysAdmin
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.admin.sys_admin import SysAdminCreate, SysAdminUpdate, SysAdminLogin, SysAdminLoginResponse

class SysAdminService:
    def create_admin(self, db: Session, request: SysAdminCreate):
        # 检查用户名是否存在
        existing_admin = db.execute(select(SysAdmin).where(SysAdmin.username == request.username)).first()
        if existing_admin:
            raise HTTPException(status_code=400, detail="用户名已存在")

        sys_admin = SysAdmin(
            username=request.username,
            # 创建管理员时，密码必须先哈希再入库。
            password=hash_password(request.password),
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
            # 修改密码时同样不能明文保存，必须重新生成哈希值。
            sys_admin.password = hash_password(request.password)
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
        # 登录流程：先查管理员，再校验密码哈希，成功后签发 JWT。
        sys_admin = db.query(SysAdmin).filter(SysAdmin.username == request.username).first()
        if not sys_admin:
            raise HTTPException(status_code=400, detail="系统管理员不存在")
        if sys_admin.status != 1:
            raise HTTPException(status_code=403, detail="当前管理员已被禁用")
        # 这里不会把明文密码解密出来，而是用明文密码去校验哈希值。
        if not verify_password(request.password, sys_admin.password):
            raise HTTPException(status_code=400, detail="密码错误")

        # sub 保存当前管理员 id；type 标识这是后台管理员 token。
        access_token = create_access_token({"sub": str(sys_admin.id), "type": "admin"})
        return SysAdminLoginResponse(access_token=access_token)