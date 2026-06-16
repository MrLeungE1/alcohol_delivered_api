from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.product_image import ProductImage
from app.schemas.admin.product import CreateProductRequest, SearchProductRequest, EditProductRequest

"""
    关于商品的业务逻辑
        基础的功能：
            1. 创建商品
            2. 商品查询
            3. 商品编辑
                1. 商品状态切换 - 上架/下架  在前端页面中可以通过switch开关进行单独改变 实质上也是编辑修改商品信息
                2. 商品分类切换
                3. 商品库存更新
            4. 商品删除
            
"""

class ProductService:
    # 创建商品
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
            cost_price=request.cost_price,
            market_price=request.market_price,
            thumb=request.thumb,
            # detail_img=request.detail_img,
            stock=request.stock,
            is_hot=request.is_hot,
            is_special=request.is_special,
            desc=request.desc,
            status=request.status,
        )
        if request.images:
            for image in request.images:
                product_image = ProductImage(
                    image_url=image.image_url,
                    image_type=image.image_type,
                    sort=image.sort,
                    product=product,
                )
                product.images.append(product_image)
        try:
            db.add(product)
            db.flush()
            db.commit()
            db.refresh(product)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"商品创建失败: {str(e)}")
        return product
    
    # 商品查询
    """
        商品查询
            目前我们有 商品名称(product_name)、商品分类(cate_id)、商品状态(status)、库存(stock)  这四个查询条件
        service中主要是将我们在routers中的方法给封装起来，方便后续的调用，所以这里函数的参数包含了
            self(当前实例对象)
            db(数据库会话)
            request(请求体参数)  这里请求体的参数需要我们在schemas中进行定义
    """
    def search_product(self, db: Session, request: SearchProductRequest):
        # 先从数据库中对商品进行查询
        query = select(Product)
        if request.product_name:
            query = query.where(Product.product_name.like(f"%{request.product_name}%"))
        if request.cate_id:
            query = query.where(Product.cate_id == request.cate_id)
        if request.status is not None:
            query = query.where(Product.status == request.status)
        if request.stock is not None:
            query = query.where(Product.stock >= request.stock)
        products = db.scalars(query).all()
        return products

    """
        编辑商品
            先通过请求体中的id 在数据库中检索对应的数据，并根据请求体中的参数进行更新
    """
    def edit_product(self, db: Session, request: EditProductRequest):
        product = db.scalar(select(Product).where(Product.id == request.id))
        if not product:
            raise HTTPException(status_code=400, detail="商品不存在")

        update_data = request.model_dump(exclude_unset=True, exclude={"id", "images"})
        for field, value in update_data.items():
            setattr(product, field, value)
        if request.images:
            for image in request.images:
                product_image = ProductImage(
                    image_url=image.image_url,
                    image_type=image.image_type,
                    sort=image.sort,
                    product=product,
                )
                product.images.append(product_image)

        try:
            db.commit()
            db.refresh(product)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"商品编辑失败: {str(e)}")
        return product

    """
        删除商品
    先通过请求体中的id 在数据库中检索对应的数据，若存在则删除，否则抛出异常
    """
    def delete_product(self, db: Session, product_id: int):
        product = db.scalar(select(Product).where(Product.id == product_id))
        if not product:
            raise HTTPException(status_code=400, detail="商品不存在")
        try:
            db.delete(product)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"商品删除失败: {str(e)}")
        return {"message": "商品删除成功"}

    # 查询商品详情
    def get_product(self, db: Session, product_id: int):
        product = db.scalar(select(Product).where(Product.id == product_id))
        if not product:
            raise HTTPException(status_code=400, detail="商品不存在")
        return product
