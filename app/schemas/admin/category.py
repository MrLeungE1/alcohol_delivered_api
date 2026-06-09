from pydantic import BaseModel, Field
from app.models.product_category import ProductCategory



class CreateCategoryRequest(BaseModel):
    cate_name: str 
    sort: int = 0  # 排序
    status: int = 1  # 状态 1:正常 2:禁用

class CategoryListRequest(BaseModel):
    cate_name: str | None = None
    sort: int | None = None
    status: int | None = None

class CategoryResponse(BaseModel):
    id: int
    cate_name: str
    sort: int
    status: int

class UpdateCategoryRequest(BaseModel):
    id: int
    cate_name: str
    sort: int = 0  # 排序
    status: int = 1  # 状态 1:正常 2:禁用

class SortCategory(BaseModel):
    sort: int
    id: int

class SortCategoryRequest(BaseModel):
    list: list[SortCategory]