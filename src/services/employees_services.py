from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.employees_dao import Employee, Task, EmployeeDao
from src.services.schemas import (
    BaseEmployeeSchema, TaskSchema, EmployeeUpdateSchema)


class EmployeeService:
    """The EmployeeDao class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the EmployeeDao class"""

        self.employee_dao = EmployeeDao()
        self.model = Employee
        self.tasks = Task

    async def get_all_employees(self, db: AsyncSession):
        """This method retrieves all employees from the database"""
        try:
            employees = await self.employee_dao.get_all_employees(db)
            return employees
        except Exception as e:
            print(f'Can not get employees: {e}')
            return []

    async def create_employee(
            self, db: AsyncSession, employee_data: BaseEmployeeSchema):
        """Create a new employee record in the database"""
        try:
            existing_employee = await self.employee_dao.get_by_name(
                db, employee_data.name
            )
            if existing_employee:
                raise ValueError(
                    f'Employee with name {employee_data.name} already exists')

            created_employee = await self.employee_dao.create_employee(
                db, employee_data
            )
            return created_employee
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f'Can not create employee: {e}'
            )

    async def get_employee(self, db: AsyncSession, employee_id):
        """ This method retrieves a specific employee
        from the database based on their ID"""
        try:
            return await self.employee_dao.get_employee(db, employee_id)
        except Exception as e:
            print(f'Can not get employee: {e}')
            return None

    async def update_employee(
            self, db: AsyncSession, employee_id,
            employees_data: EmployeeUpdateSchema):
        """ This method updates an existing employee record in the database"""
        try:
            existing_employee = await self.employee_dao.get_by_name(
                db, employees_data.name
            )
            if existing_employee and existing_employee.id != employee_id:
                raise ValueError(
                    f'Employee with name {employees_data.name} already exists')
            return await self.employee_dao.update_employee(
                db, employee_id, employees_data
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f'Can not update employee: {e}'
            )

    async def delete_employee(self, db: AsyncSession, employee_id):
        """ This method deletes an employee record from the database"""

        return await self.employee_dao.delete_employee(db, employee_id)

    async def get_employees_busy(self, db: AsyncSession):
        """ This method retrieves all employees with active tasks"""
        employees_with_active_tasks = await (
            self.employee_dao.get_employees_busy(db))
        return employees_with_active_tasks

    async def find_least_loaded_employee(
            self, db: AsyncSession, task: TaskSchema
    ):
        """ This method retrieves the employee with the least loaded tasks"""
        employee = await self.employee_dao.find_least_loaded_employee(db, task)
        return employee
