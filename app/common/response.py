from __future__ import annotations

from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


SUCCESS_MESSAGE = "请求成功"


def build_response(
    data: Any = None,
    code: int = 200,
    msg: str = SUCCESS_MESSAGE,
    status_code: int | None = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code or code,
        content={
            "code": code,
            "msg": msg,
            "data": jsonable_encoder(data),
        },
    )


def is_standard_response(data: Any) -> bool:
    return (
        isinstance(data, dict)
        and set(data.keys()) == {"code", "msg", "data"}
    )
