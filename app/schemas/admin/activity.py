from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class CreateActivityRequest(BaseModel):
    activity_name: str
    banner: str
    start_time: datetime
    end_time: datetime
    status: int = 1
    product_ids: List[int] = Field(default_factory=list)
    desc: str = ""

    class Config:
        orm_mode = True

class EditActivityRequest(BaseModel):
    id: int
    activity_name: str
    banner: str
    start_time: datetime
    end_time: datetime
    status: int = 1
    product_ids: List[int] = Field(default_factory=list)
    desc: str = ""

    class Config:
        orm_mode = True