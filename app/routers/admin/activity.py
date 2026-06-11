from fastapi import APIRouter, Depends
from app.schemas.admin.activity import CreateActivityRequest, EditActivityRequest
from app.services.admin.activity import ActivityService
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(prefix="/activity", tags=["活动管理"])

@router.post("/create", summary="新建活动")
def create_activity(request: CreateActivityRequest, db: Session = Depends(get_db)):
    return ActivityService.create_activity(db, request)

@router.put("/edit", summary="编辑活动")
def edit_activity(request: EditActivityRequest, db: Session = Depends(get_db)):
    return ActivityService.edit_activity(db, request)

@router.delete("/{activity_id}", summary="删除活动")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    return ActivityService.delete_activity(db, activity_id)
