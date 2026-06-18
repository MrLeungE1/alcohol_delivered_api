from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.models.activity_product import ActivityProduct
from app.models.product import Product
from app.schemas.admin.activity import CreateActivityRequest, EditActivityRequest

class ActivityService:
    @staticmethod
    def _validate_products(db: Session, product_ids: list[int]):
        if not product_ids:
            return
        products = db.scalars(select(Product).where(Product.id.in_(product_ids))).all()
        if len(products) != len(set(product_ids)):
            raise HTTPException(status_code=400, detail="存在无效的商品ID")

    @staticmethod
    def create_activity(db: Session, request: CreateActivityRequest):
        ActivityService._validate_products(db, request.product_ids)
        activity = Activity(
            activity_name=request.activity_name,
            banner=request.banner,
            start_time=request.start_time,
            end_time=request.end_time,
            status=request.status,
            desc=request.desc,
        )
        try:
            db.add(activity)
            db.flush()
            for product_id in set(request.product_ids):
                db.add(ActivityProduct(activity_id=activity.id, product_id=product_id))
            db.commit()
            db.refresh(activity)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"活动创建失败: {str(e)}")
        return activity

    @staticmethod
    def edit_activity(db: Session, request: EditActivityRequest):
        activity = db.scalar(select(Activity).where(Activity.id == request.id))
        if not activity:
            raise HTTPException(status_code=400, detail="活动不存在")
        ActivityService._validate_products(db, request.product_ids)
        activity.activity_name = request.activity_name
        activity.banner = request.banner
        activity.start_time = request.start_time
        activity.end_time = request.end_time
        activity.status = request.status
        activity.desc = request.desc
        try:
            db.execute(delete(ActivityProduct).where(ActivityProduct.activity_id == activity.id))
            for product_id in set(request.product_ids):
                db.add(ActivityProduct(activity_id=activity.id, product_id=product_id))
            db.commit()
            db.refresh(activity)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"活动编辑失败: {str(e)}")
        return activity

    @staticmethod
    def delete_activity(db: Session, activity_id: int):
        activity = db.scalar(select(Activity).where(Activity.id == activity_id))
        if not activity:
            raise HTTPException(status_code=400, detail="活动不存在")
        # 活动删除需要查看当前活动是否有商品关联
        activity_products = db.scalars(select(ActivityProduct).where(ActivityProduct.activity_id == activity_id)).all()
        if activity_products:
            raise HTTPException(status_code=400, detail="活动下有商品关联，不能删除")
        try:
            db.delete(activity)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"活动删除失败: {str(e)}")
        return {"message": "活动删除成功"}

    @staticmethod
    def get_all_activities(db: Session):
        return db.scalars(select(Activity)).all()