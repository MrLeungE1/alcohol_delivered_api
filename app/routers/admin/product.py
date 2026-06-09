from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.admin.product import ProductService
from app.schemas.admin.product import CreateProductRequest, ProductResponse, SearchProductRequest, EditProductRequest
from typing import List

router = APIRouter(prefix="/admin/product", tags=["商品管理"])
product_service = ProductService()

@router.post("/add", response_model=ProductResponse, status_code=201, summary="创建商品")
def add_product(request: CreateProductRequest, db: Session = Depends(get_db)):
    return product_service.create_product(db, request)

@router.post("/search", response_model=List[ProductResponse], summary="查询商品")
def search_products(request: SearchProductRequest, db: Session = Depends(get_db)):
    return product_service.search_product(db, request)

@router.put("/edit", response_model=ProductResponse, summary="编辑商品")
def edit_product(request: EditProductRequest, db: Session = Depends(get_db)):
    return product_service.edit_product(db, request)

@router.delete("/{product_id}", summary="删除商品")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.delete_product(db, product_id)

@router.get("/product/{product_id}", summary="查询商品详情")
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, product_id)
