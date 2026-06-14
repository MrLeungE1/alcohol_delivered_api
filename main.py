import json
import os

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.common.response import build_response, is_standard_response
from app.core.config import settings
from app.db.init_db import init_database
from app.routers.admin.activity import router as activity_router
from app.routers.admin.category import router as category_router
from app.routers.admin.product import router as product_router
from app.routers.admin.sys_admin import router as sys_admin_router
from app.routers.wx.product import router as wx_product_router
from app.routers.upload import router as upload_router

init_database()

app = FastAPI(title="酒水配送系统")

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")

app.include_router(upload_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(sys_admin_router)
app.include_router(activity_router)
app.include_router(wx_product_router)

SKIP_WRAP_PATHS = ("/docs", "/redoc", "/openapi.json", "/static")


@app.middleware("http")
async def unify_response(request: Request, call_next):
    response = await call_next(request)

    if request.url.path.startswith(SKIP_WRAP_PATHS):
        return response

    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        return response

    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    if not body:
        return build_response(code=200, status_code=response.status_code)

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    if is_standard_response(payload):
        headers = dict(response.headers)
        headers.pop("content-length", None)
        return JSONResponse(
            status_code=response.status_code,
            content=payload,
            headers=headers,
        )

    headers = dict(response.headers)
    headers.pop("content-length", None)

    if response.status_code >= 400:
        message = "请求失败"
        data = None
        if isinstance(payload, dict) and "detail" in payload:
            detail = payload["detail"]
            if isinstance(detail, str):
                message = detail
            else:
                data = detail
        else:
            data = payload
        return JSONResponse(
            status_code=response.status_code,
            content={
                "code": response.status_code,
                "msg": message,
                "data": data,
            },
            headers=headers,
        )

    return JSONResponse(
        status_code=response.status_code,
        content={
            "code": 200,
            "msg": "请求成功",
            "data": payload,
        },
        headers=headers,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return build_response(
        code=exc.status_code,
        msg=str(exc.detail),
        data=None,
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return build_response(
        code=422,
        msg="请求参数校验失败",
        data=exc.errors(),
        status_code=422,
    )


@app.exception_handler(Exception)
async def common_exception_handler(request: Request, exc: Exception):
    return build_response(
        code=500,
        msg="服务器内部错误",
        data=None,
        status_code=500,
    )

@app.get("/")
def read_root():
    return {"message": "Hello World"}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8091)
