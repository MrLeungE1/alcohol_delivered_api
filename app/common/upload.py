import os
import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException
from app.core.config import settings

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_image(file: UploadFile):
    ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {ext}，仅支持 {','.join(ALLOWED_EXTENSIONS)}")


def save_upload(file: UploadFile, sub_dir: str = "common") -> str:
    validate_image(file)

    contents = file.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过5MB")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    date_path = datetime.now().strftime("%Y/%m")
    dir_path = os.path.join(settings.UPLOAD_DIR, sub_dir, date_path)
    os.makedirs(dir_path, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(dir_path, filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    url = f"/static/{sub_dir}/{date_path}/{filename}"
    return url