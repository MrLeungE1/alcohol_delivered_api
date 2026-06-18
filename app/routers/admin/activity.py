from fastapi import APIRouter, Depends
from app.schemas.admin.activity import CreateActivityRequest, EditActivityRequest
from app.services.admin.activity import ActivityService
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.depend import get_current_admin

router = APIRouter(prefix="/activity", tags=["活动管理"])

@router.post("/create", summary="新建活动")
def create_activity(request: CreateActivityRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 活动管理属于后台管理能力，进入函数前会先校验 Bearer token。
    return ActivityService.create_activity(db, request)

@router.put("/edit", summary="编辑活动")
def edit_activity(request: EditActivityRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # current_admin 参数本身就代表“必须是已登录管理员才能访问”。
    return ActivityService.edit_activity(db, request)

@router.delete("/{activity_id}", summary="删除活动")
def delete_activity(activity_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 删除活动前必须完成鉴权，避免匿名用户删除后台数据。
    return ActivityService.delete_activity(db, activity_id)

@router.get("/list", summary="获取所有活动")
def get_all_activities(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 获取所有活动前必须完成鉴权，避免匿名用户查看后台数据。
    return ActivityService.get_all_activities(db)
