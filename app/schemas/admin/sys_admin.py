from pydantic import BaseModel
from app.models.sys_admin import SysAdmin

class SysAdminCreate(BaseModel):
    username: str
    password: str
    name: str = None
    status: int = 1

class SysAdminUpdate(BaseModel):
    id: int
    username: str = None
    password: str = None
    name: str = None
    status: int = None

class SysAdminLogin(BaseModel):
    username: str
    password: str

class SysAdminLoginResponse(BaseModel):
    token: str