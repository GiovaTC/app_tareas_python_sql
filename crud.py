# backend/crud.py
from sqlalchemy.orm import Session
import models

def get_tasks(db: Session):
    return db.query(models.Task).all()

def create_task(db: Session, title: str):
    task = models.Task(title = title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task). filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()

def complete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.completed = True
        db.commit()
