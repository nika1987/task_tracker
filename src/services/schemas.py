from typing import ForwardRef
from pydantic import BaseModel, Field


TaskRef = ForwardRef('BaseTaskSchema')


class BaseEmployeeSchema(BaseModel):
    """ The base schema to work with employees data"""
    name: str
    positions: str
    department: str

    class Config:
        from_attributes = True


class BaseTaskSchema(BaseModel):
    """ The base schema to work with employees data"""
    title: str
    description: str
    status: str
    is_important: bool
    employee_id: int | None = None
    parent_task_id: int | None = None

    class Config:
        from_attributes = True


class EmployeesSchema(BaseEmployeeSchema):
    """This schema used as serializer to get a list of employees"""
    id: int


class EmployeeCreateUpdateSchema(BaseEmployeeSchema):
    """ The base schema with additional methods"""


class EmployeeUpdateSchema(BaseEmployeeSchema):
    """ The base schema with additional methods"""
    name: str | None = None
    positions: str | None = None
    department: str | None = None


class TaskSchema(BaseTaskSchema):
    """This schema used as serializer to get a list of tasks"""
    id: int


class TaskCreateUpdateSchema(BaseTaskSchema):
    """ The base schema with additional methods"""


class TaskUpdateSchema(BaseTaskSchema):
    """ The base schema with additional methods"""
    title: str | None = None
    description: str | None = None
    status: str | None = None
