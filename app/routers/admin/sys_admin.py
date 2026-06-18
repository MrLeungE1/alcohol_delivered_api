from fastapi import APIRouter, Depends
from app.models.sys_admin import SysAdmin
from sqlalchemy.orm import Session
from app.services.admin.sys_admin import SysAdminService
from app.schemas.admin.sys_admin import SysAdminCreate, SysAdminUpdate, SysAdminLogin, SysAdminLoginResponse
from app.db.session import get_db
from app.core.depend import get_current_admin

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
    # 登录接口本身不需要 token；它的作用就是校验账号密码并返回 token。
    return sys_admin.login_admin(db, request)

@router.get('/me', summary="获取当前登录管理员")
def get_current_admin_info(current_admin: SysAdmin = Depends(get_current_admin)):
    # 这个接口依赖 get_current_admin，所以请求时必须在请求头中携带 Bearer token。
    return {
        "id": current_admin.id,
        "username": current_admin.username,
        "name": current_admin.name,
        "status": current_admin.status,
    }
