from fastapi import APIRouter, Depends
from app.models.product_category import ProductCategory
from app.schemas.admin.category import CreateCategoryRequest, CategoryResponse, UpdateCategoryRequest, CategoryListRequest, SortCategoryRequest
from app.services.admin.category import CategoryService
from sqlalchemy.orm import Session
from app.db.session import get_db
from fastapi import HTTPException
from app.core.depend import get_current_admin

router = APIRouter(prefix="/category", tags=["商品类别"])
category_service = CategoryService()

@router.post("/add", response_model=CategoryResponse, summary="添加商品类别")
def create_category(request: CreateCategoryRequest,db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 分类管理是后台操作，所以这里要求前端在请求头中携带管理员 token。
    return category_service.create_category(db, request)

@router.put("/edit", response_model=CategoryResponse, summary="更新商品类别")
def update_category(request:UpdateCategoryRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # Depends(get_current_admin) 会先完成鉴权，鉴权失败时这里不会继续执行。
    return category_service.update_category(db, request)

@router.post("/list", response_model=list[CategoryResponse], summary="获取商品类别列表")
def get_category_list(request: CategoryListRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 后台列表接口也受 token 保护，避免未登录用户读取后台数据。
    return category_service.get_category_list(db, request)

@router.delete("/{request_id}", summary="删除商品类别")
def del_category(request_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 删除属于敏感操作，必须通过管理员鉴权。
    return category_service.del_category(db, request_id)

@router.post("/sort", summary="排序商品类别")
def sort_category(request: SortCategoryRequest, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    # 排序会影响后台展示结果，所以同样只允许已登录管理员访问。
    return category_service.sort_category(db, request)