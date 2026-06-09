from fastapi import FastAPI
from app.db.init_db import init_database
from app.routers.admin.product import router as product_router
from app.routers.admin.category import router as category_router
from app.routers.admin.sys_admin import router as sys_admin_router
init_database()

app = FastAPI()
app.include_router(product_router)
app.include_router(category_router)
app.include_router(sys_admin_router)

@app.get("/")
def read_root():
    return {"message": "Hello World"}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8091)
