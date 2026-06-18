from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

# 统一管理后台密码哈希算法。
# 新密码默认使用 pbkdf2_sha256；同时保留 bcrypt，兼容旧密码哈希校验。
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    # 密码入库前先做哈希，数据库只保存哈希值，不保存明文密码。
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 登录时用用户输入的明文密码去校验数据库中的哈希值。
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    # 生成后台 access_token。
    # token 内会保存管理员 id、类型以及过期时间，后续接口据此识别当前登录人。
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    # 解析并校验 token 签名与有效期；失败时会抛出异常，由依赖层统一处理。
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])