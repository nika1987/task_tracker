from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import Any


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


class EmployeesSchema(BaseEmployeeSchema):
    """This schema used as serializer to get a list of tables"""

    class Config:
        orm_mode = True


class EmployeeChangeSchema(BaseEmployeeSchema):
    """ The base schema with additional methods"""

    def promote_employee(self, new_position):
        self.positions = new_position

    def delete_employee(self):
        fields_to_delete = ['name', 'positions', 'department']
        for field in fields_to_delete:
            self.__dict__.pop(field, None)


class TaskChangeSchema(BaseTaskSchema):
    """ The base schema with additional methods"""

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.task = None

    def promote_task(self, new_task):
        self.task = new_task

    def delete_task_fields(self):
        fields_to_delete = ['title', 'description', 'status']
        for field in fields_to_delete:
            self.dict.pop(field, None)
