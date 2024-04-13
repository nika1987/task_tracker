import sqlalchemy as sqa
from sqlalchemy.orm import relationship
from dao import Base


class Employees(Base):
    __tablename__ = "employees"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    name = sqa.Column(sqa.String)
    positions = sqa.Column(sqa.String)
    department = sqa.Column(sqa.String)
    tasks = relationship("Tasks", back_populates='employee')


class Tasks(Base):
    __tablename__ = "tasks"
    id = sqa.Column(sqa.Integer, primary_key=True, autoincrement=True)
    title = sqa.Column(sqa.String)
    description = sqa.Column(sqa.String)
    status = sqa.Column(sqa.String)
    employee_id = sqa.Column(sqa.Integer)
    employees = relationship("Employees", back_populates='tasks')
