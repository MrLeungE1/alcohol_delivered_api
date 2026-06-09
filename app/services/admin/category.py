from app.models.product_category import ProductCategory
from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.admin.category import CreateCategoryRequest, UpdateCategoryRequest, CategoryListRequest

# 公共函数 验证名称是否存在
def verify_category_name(db: Session, cate_name: str, exclude_id: int = None):
    query = select(ProductCategory).where(ProductCategory.cate_name == cate_name)
    if exclude_id:
        query = query.where(ProductCategory.id != exclude_id)
    category = db.scalar(query)
    if category:
        raise HTTPException(status_code=400, detail="商品类别已存在")

class CategoryService:
    def create_category(self, db: Session, request: CreateCategoryRequest):
        verify_category_name(db, request.cate_name)
        new_category = ProductCategory(
            cate_name=request.cate_name,
            sort=request.sort,
            status=request.status,
        )
        try:
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        return new_category
    
    def update_category(self, db: Session, request: UpdateCategoryRequest):
        category = db.scalar(
            select(ProductCategory).where(ProductCategory.id == request.id)
        )
        if not category:
            raise HTTPException(status_code=404, detail="商品类别不存在")
        verify_category_name(db, request.cate_name, exclude_id=request.id)
        category.cate_name = request.cate_name
        category.sort = request.sort
        category.status = request.status
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        return category

    def get_category_list(self, db: Session, request: CategoryListRequest):
        query = select(ProductCategory)
        if request.status is not None:
            query = query.where(ProductCategory.status == request.status)
            
        if request.cate_name:
            query = query.where(ProductCategory.cate_name.contains(request.cate_name))
        
        # 核心：固定排序，不能动态判断
        query = query.order_by(ProductCategory.sort.asc())
        categories = db.scalars(query).all()
        return categories

    def del_category(self, db: Session, request_id: int):
        category = db.scalar(
            select(ProductCategory).where(ProductCategory.id == request_id)
        )
        if not category:
            raise HTTPException(status_code=404, detail="商品类别不存在")
        try: 
            db.delete(category)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        return category
    
    def sort_category(self, db: Session, request: SortCategoryRequest):
        for item in request.list:
            category = db.scalar(
                select(ProductCategory).where(ProductCategory.id == item.id)
            )
            if not category:
                raise HTTPException(status_code=404, detail="商品类别不存在")
            category.sort = item.sort
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        return request.list