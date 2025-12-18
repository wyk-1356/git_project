from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.group import GroupCreate, GroupUpdate, GroupResponse
from app.crud import group as group_crud
from app.crud import student as student_crud
from app.schemas.student import StudentResponse

router = APIRouter()

@router.post("/", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    """Создать новую группу"""
    return group_crud.create_group(db=db, group=group)

@router.get("/{group_id}", response_model=GroupResponse)
def read_group(group_id: int, db: Session = Depends(get_db)):
    """Получить информацию о группе по ее ID"""
    db_group = group_crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

@router.get("/", response_model=List[GroupResponse])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех групп"""
    groups = group_crud.get_groups(db, skip=skip, limit=limit)
    return groups

@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: int, group_update: GroupUpdate, db: Session = Depends(get_db)):
    """Обновить информацию о группе"""
    db_group = group_crud.update_group(db, group_id=group_id, group_update=group_update)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

@router.delete("/{group_id}", response_model=GroupResponse)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    """Удалить группу"""
    db_group = group_crud.delete_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return db_group

@router.get("/{group_id}/students", response_model=List[StudentResponse])
def get_students_in_group(group_id: int, db: Session = Depends(get_db)):
    """Получить всех студентов в группе"""
    # Проверяем существование группы
    db_group = group_crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    
    students = student_crud.get_students_in_group(db, group_id=group_id)
    return students
