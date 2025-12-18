from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    age: Optional[int] = None
    group_id: Optional[int] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    group_id: Optional[int] = None

class StudentInDB(StudentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentResponse(StudentInDB):
    pass
