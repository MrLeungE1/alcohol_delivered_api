from fastapi import APIRouter, Depends
from app.models.sys_admin import SysAdmin
from sqlalchemy.orm import Session
from app.services.admin.sys_admin import SysAdminService
from app.schemas.admin.sys_admin import SysAdminCreate, SysAdminUpdate, SysAdminLogin, SysAdminLoginResponse
from app.db.session import get_db

# 系统管理员路由
router = APIRouter(prefix="/admin/sys_admin", tags=["系统管理"])
sys_admin = SysAdminService()

@router.post('/create', response_model=SysAdminCreate, summary="新建用户")
def create_sys_admin(request: SysAdminCreate, db: Session = Depends(get_db)):
    return sys_admin.create_admin(db, request)

@router.post('/update', response_model=SysAdminCreate, summary="更新用户")
def update_sys_admin(request: SysAdminUpdate, db: Session = Depends(get_db)):
    return sys_admin.update_admin(db, request)

@router.post('/login', response_model=SysAdminLoginResponse, summary="用户登录")
def login_sys_admin(request: SysAdminLogin, db: Session = Depends(get_db)):
    return sys_admin.login_admin(db, request)
