from sqlalchemy.orm import Session
from app.models import Group
from app.schemas.group import GroupCreate, GroupUpdate
from typing import List

def get_group(db: Session, group_id: int):
    """Получить группу по ID"""
    return db.query(Group).filter(Group.id == group_id).first()

def get_groups(db: Session, skip: int = 0, limit: int = 100):
    """Получить список групп с пагинацией"""
    return db.query(Group).offset(skip).limit(limit).all()

def create_group(db: Session, group: GroupCreate):
    """Создать новую группу"""
    db_group = Group(
        name=group.name,
        description=group.description
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_group(db: Session, group_id: int, group_update: GroupUpdate):
    """Обновить информацию о группе"""
    db_group = get_group(db, group_id)
    if db_group:
        update_data = group_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_group, key, value)
        db.commit()
        db.refresh(db_group)
    return db_group

def delete_group(db: Session, group_id: int):
    """Удалить группу"""
    db_group = get_group(db, group_id)
    if db_group:
        db.delete(db_group)
        db.commit()
    return db_group
