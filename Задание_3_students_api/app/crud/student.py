from sqlalchemy.orm import Session
from app.models import Student
from app.schemas.student import StudentCreate, StudentUpdate
from typing import List, Optional

def get_student(db: Session, student_id: int):
    """Получить студента по ID"""
    return db.query(Student).filter(Student.id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    """Получить список студентов с пагинацией"""
    return db.query(Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: StudentCreate):
    """Создать нового студента"""
    db_student = Student(
        full_name=student.full_name,
        email=student.email,
        age=student.age,
        group_id=student.group_id
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student_update: StudentUpdate):
    """Обновить информацию о студенте"""
    db_student = get_student(db, student_id)
    if db_student:
        update_data = student_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    """Удалить студента"""
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student

def add_student_to_group(db: Session, student_id: int, group_id: int):
    """Добавить студента в группу"""
    db_student = get_student(db, student_id)
    if db_student:
        db_student.group_id = group_id
        db.commit()
        db.refresh(db_student)
    return db_student

def remove_student_from_group(db: Session, student_id: int):
    """Удалить студента из группы"""
    db_student = get_student(db, student_id)
    if db_student:
        db_student.group_id = None
        db.commit()
        db.refresh(db_student)
    return db_student

def get_students_in_group(db: Session, group_id: int):
    """Получить всех студентов в группе"""
    return db.query(Student).filter(Student.group_id == group_id).all()

def transfer_student(db: Session, student_id: int, from_group_id: int, to_group_id: int):
    """Перевести студента из группы A в группу B"""
    db_student = get_student(db, student_id)
    if db_student and db_student.group_id == from_group_id:
        db_student.group_id = to_group_id
        db.commit()
        db.refresh(db_student)
    return db_student
