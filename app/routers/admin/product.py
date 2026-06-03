from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.admin.product import ProductService
from app.schemas.admin.product import CreateProductRequest, ProductResponse

router = APIRouter(prefix="/admin/product")
product_service = ProductService()

@router.post("/add", response_model=ProductResponse, status_code=201)
def add_product(request: CreateProductRequest, db: Session = Depends(get_db)):
    return product_service.create_product(db, request)
