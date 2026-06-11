from fastapi import APIRouter, UploadFile, File, Query
from app.common.upload import save_upload

router = APIRouter(prefix="/upload", tags=["通用上传"])

@router.post("/upload",  summary="通用上传图片")
def upload_common_file(
    file: UploadFile = File(..., description="上传的图片文件"), 
    module: str = Query(..., description="模块名， product/activity/home")
):
    url = save_upload(file, sub_dir=module)
    return {"url": url}