from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.crud import student as student_crud
from app.crud import group as group_crud

router = APIRouter()

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Создать нового студента"""
    return student_crud.create_student(db=db, student=student)

@router.get("/{student_id}", response_model=StudentResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    """Получить информацию о студенте по его ID"""
    db_student = student_crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.get("/", response_model=List[StudentResponse])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Получить список всех студентов"""
    students = student_crud.get_students(db, skip=skip, limit=limit)
    return students

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    """Обновить информацию о студенте"""
    db_student = student_crud.update_student(db, student_id=student_id, student_update=student_update)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента"""
    db_student = student_crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.post("/{student_id}/group/{group_id}", response_model=StudentResponse)
def add_student_to_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    """Добавить студента в группу"""
    # Проверяем существование группы
    db_group = group_crud.get_group(db, group_id=group_id)
    if db_group is None:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    
    db_student = student_crud.add_student_to_group(db, student_id=student_id, group_id=group_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.delete("/{student_id}/group", response_model=StudentResponse)
def remove_student_from_group(student_id: int, db: Session = Depends(get_db)):
    """Удалить студента из группы"""
    db_student = student_crud.remove_student_from_group(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return db_student

@router.post("/{student_id}/transfer/{from_group_id}/{to_group_id}", response_model=StudentResponse)
def transfer_student(student_id: int, from_group_id: int, to_group_id: int, db: Session = Depends(get_db)):
    """Перевести студента из группы A в группу B"""
    # Проверяем существование групп
    db_from_group = group_crud.get_group(db, group_id=from_group_id)
    db_to_group = group_crud.get_group(db, group_id=to_group_id)
    
    if db_from_group is None or db_to_group is None:
        raise HTTPException(status_code=404, detail="Одна из групп не найдена")
    
    db_student = student_crud.transfer_student(
        db, 
        student_id=student_id, 
        from_group_id=from_group_id, 
        to_group_id=to_group_id
    )
    if db_student is None:
        raise HTTPException(status_code=404, detail="Студент не найден или не в указанной группе")
    return db_student
