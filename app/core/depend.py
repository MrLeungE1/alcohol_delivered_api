from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.sys_admin import SysAdmin

# HTTPBearer 会从请求头中读取：Authorization: Bearer <token>
bearer_scheme = HTTPBearer()


def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> SysAdmin:
    # 所有依赖了 get_current_admin 的后台接口，都会先走这段逻辑。
    # 也就是说：后台接口想访问成功，必须先在请求头里携带合法 token。
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        admin_id = payload.get("sub")
        token_type = payload.get("type")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="登录已失效，请重新登录")

    # sub 保存管理员 id，type 用来区分当前 token 是不是后台管理员 token。
    if not admin_id or token_type != "admin":
        raise HTTPException(status_code=401, detail="无效的登录凭证")

    # 再从数据库查一次管理员，避免“token 合法但账号已删除/禁用”的情况。
    admin = db.query(SysAdmin).filter(SysAdmin.id == int(admin_id)).first()
    if not admin:
        raise HTTPException(status_code=401, detail="当前管理员不存在")
    if admin.status != 1:
        raise HTTPException(status_code=403, detail="当前管理员已被禁用")
    return admin