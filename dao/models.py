import sqlalchemy as sqa

from sqlalchemy.orm import relationship
from dao import Base


class Employee(Base):
    __tablename__ = "employees"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    name = sqa.Column(sqa.String)
    positions = sqa.Column(sqa.String)
    department = sqa.Column(sqa.String)
    task = relationship("Task", back_populates='employee')


class Task(Base):
    __tablename__ = "tasks"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    title = sqa.Column(sqa.String)
    description = sqa.Column(sqa.String)
    status = sqa.Column(sqa.String)
    employee_id = sqa.Column(sqa.Integer, sqa.ForeignKey('employees.id'))
    parent_task_id = sqa.Column(sqa.Integer, sqa.ForeignKey('tasks.id'))

    employee = relationship("Employee", back_populates='tasks')
    parent_task = relationship("Task", remote_side=[id], back_populates='child_task')
    child_task = relationship("Task", back_populates='parent_task')
