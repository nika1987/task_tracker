import sqlalchemy as sqa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from dao import Base


class Employee(Base):
    __tablename__ = "employees"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    name = sqa.Column(sqa.String)
    positions = sqa.Column(sqa.String)
    department = sqa.Column(sqa.String)
    tasks = relationship("Tasks", back_populates='employee')


class Task(Base):
    __tablename__ = "tasks"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    title = sqa.Column(sqa.String)
    description = sqa.Column(sqa.String)
    status = sqa.Column(sqa.String)
    employee_id = sqa.Column(sqa.Integer, ForeignKey('employees.id'))
    parent_task_id = sqa.Column(sqa.Integer, ForeignKey('tasks.id'))

    employees = relationship("Employees", back_populates='tasks')
    parent_task = relationship("Tasks", remote_side=[id], back_populates='child_tasks')
