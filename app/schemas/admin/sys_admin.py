from pydantic import BaseModel, Field

class SysAdminCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=128)
    name: str = None
    status: int = 1

    model_config = {"from_attributes": True}

class SysAdminUpdate(BaseModel):
    id: int
    username: str = None
    password: str = Field(None, min_length=6, max_length=128)
    name: str = None
    status: int = None

    model_config = {"from_attributes": True}

class SysAdminLogin(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=128)

class SysAdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"