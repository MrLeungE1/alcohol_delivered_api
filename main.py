from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db.init_db import init_database
from app.routers.admin.product import router as product_router
from app.routers.admin.category import router as category_router
from app.routers.admin.sys_admin import router as sys_admin_router
from app.routers.upload import router as upload_router
from app.routers.admin.activity import router as activity_router
from app.core.config import settings
import os
init_database()

app = FastAPI(title="酒水配送系统")

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")

app.include_router(upload_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(sys_admin_router)
app.include_router(activity_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8091)
