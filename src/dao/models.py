from datetime import datetime

import sqlalchemy as sqa

from sqlalchemy.orm import relationship
from src.dao import Base


class Employee(Base):
    """The Employee model to get data from the database"""
    __tablename__ = "employees"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    name = sqa.Column(sqa.String, unique=True)
    positions = sqa.Column(sqa.String)
    department = sqa.Column(sqa.String)
    tasks = relationship("Task", back_populates='employee', lazy='joined')


class Task(Base):
    """The Task model to get data from the database"""
    __tablename__ = "tasks"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    title = sqa.Column(sqa.String)
    description = sqa.Column(sqa.String)
    deadline = sqa.Column(sqa.DateTime, default=datetime.now)
    status = sqa.Column(sqa.String)
    is_important = sqa.Column(sqa.Boolean, default=False)
    employee_id = sqa.Column(
        sqa.Integer, sqa.ForeignKey('employees.id'), nullable=True)
    parent_task_id = sqa.Column(
        sqa.Integer, sqa.ForeignKey('tasks.id'), nullable=True, default=lambda: None)

    employee = relationship("Employee", back_populates='tasks', lazy='joined')
    child_tasks = relationship(
        "Task", back_populates='parent_task', lazy='joined',
    )
    parent_task = relationship(
        "Task", remote_side='Task.id', back_populates='child_tasks',
        foreign_keys=[parent_task_id], lazy='joined')
