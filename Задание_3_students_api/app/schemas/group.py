from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.student import StudentResponse

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class GroupInDB(GroupBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class GroupResponse(GroupInDB):
    students: List[StudentResponse] = []
