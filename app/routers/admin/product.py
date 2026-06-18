from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.admin.product import ProductService
from app.schemas.admin.product import CreateProductRequest, ProductResponse, SearchProductRequest, EditProductRequest
from typing import List
from app.core.depend import get_current_admin

router = APIRouter(prefix="/admin/product", tags=["商品管理"])
product_service = ProductService()

@router.post("/add", response_model=ProductResponse, status_code=201, summary="创建商品")
def add_product(request: CreateProductRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 只要参数里写了 Depends(get_current_admin)，这个接口就必须携带管理员 token。
    # current_admin 已经是当前登录管理员对象，这里暂时不用它，但它完成了鉴权。
    return product_service.create_product(db, request)

@router.post("/search", response_model=List[ProductResponse], summary="查询商品")
def search_products(request: SearchProductRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 商品管理属于后台能力，因此查询接口也要求先登录。
    return product_service.search_product(db, request)

@router.put("/edit", response_model=ProductResponse, summary="编辑商品")
def edit_product(request: EditProductRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 编辑商品前先校验管理员身份，防止未登录用户直接修改后台数据。
    return product_service.edit_product(db, request)

@router.delete("/{product_id}", summary="删除商品")
def delete_product(product_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 删除类接口风险更高，必须要求 token，不能让匿名请求直接访问。
    return product_service.delete_product(db, product_id)

@router.get("/product/{product_id}", summary="查询商品详情")
def get_product(product_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 这里同样依赖管理员 token，保证后台详情接口只对已登录管理员开放。
    return product_service.get_product(db, product_id)
