from pydantic import BaseModel


class BaseEmployeeSchema(BaseModel):
    """ The base schema to work with employees data"""
    name: str
    positions: str
    department: str

    class Config:
        orm_mode = True


class BaseTaskSchema(BaseModel):
    """ The base schema to work with employees data"""
    title: str
    description: str
    status: str
    employee_id: int
    parent_task_id: None = None

    class Config:
        orm_mode = True


class EmployeesSchema(BaseEmployeeSchema):
    """This schema used as serializer to get a list of employees"""
    id: int


class EmployeeCreateUpdateSchema(BaseEmployeeSchema):
    """ The base schema with additional methods"""


class TaskSchema(BaseTaskSchema):
    """This schema used as serializer to get a list of tasks"""
    id: int


class TaskCreateUpdateSchema(BaseTaskSchema):
    """ The base schema with additional methods"""
