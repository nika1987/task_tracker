import sqlalchemy as sqa

from sqlalchemy.orm import relationship
from dao import Base


class Employee(Base):
    __tablename__ = "employees"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    name = sqa.Column(sqa.String)
    positions = sqa.Column(sqa.String)
    department = sqa.Column(sqa.String)


class Task(Base):
    __tablename__ = "tasks"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    title = sqa.Column(sqa.String)
    description = sqa.Column(sqa.String)
    status = sqa.Column(sqa.String)
    employee_id = sqa.Column(sqa.Integer, sqa.ForeignKey('employees.id'), nullable=True)
    parent_task_id = sqa.Column(sqa.Integer, sqa.ForeignKey('tasks.id'), nullable=True)
    #child_task_id = sqa.Column(sqa.Integer, sqa.ForeignKey('tasks.id'))

    employee = relationship("Employee", backref='tasks')
    parent_task = relationship(
        "Task", remote_side='Task.id', backref='child_task',
        foreign_keys=[parent_task_id])
