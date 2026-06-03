from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.schemas.admin.product import CreateProductRequest

class ProductService:
    def create_product(self, db: Session, request: CreateProductRequest):
        cate = db.scalar(
            select(ProductCategory).where(ProductCategory.id == request.cate_id)
        )
        if not cate:
            raise HTTPException(status_code=400, detail="商品分类不存在")

        existing = db.scalar(
            select(Product).where(
                Product.cate_id == request.cate_id,
                Product.product_name == request.product_name,
            )
        )
        if existing:
            raise HTTPException(status_code=400, detail="该分类下商品名称已存在")

        product = Product(
            cate_id=request.cate_id,
            product_name=request.product_name,
            price=request.price,
            market_price=request.market_price,
            thumb=request.thumb,
            detail_img=request.detail_img,
            stock=request.stock,
            is_hot=request.is_hot,
            is_special=request.is_special,
            desc=request.desc,
            status=request.status,
        )
        try:
            db.add(product)
            db.flush()
            db.commit()
            db.refresh(product)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"商品创建失败: {str(e)}")
        return product

