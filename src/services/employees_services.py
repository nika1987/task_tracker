from sqlalchemy import select, update, delete

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.employees_dao import Employee, Task, EmployeeDao

from src.services.schemas import (BaseEmployeeSchema,
                                  EmployeeCreateUpdateSchema, EmployeesSchema,
                                  TaskSchema)


class EmployeeService:
    """The EmployeeDao class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the EmployeeDao class"""

        self.employee_dao = EmployeeDao()
        self.model = Employee
        self.tasks = Task

    async def get_all_employees(self, db: AsyncSession):
        """This method retrieves all employees from the database"""
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            employees = result.unique().scalars().all()
            return employees

    async def create_employee(
            self, db: AsyncSession,
            employee_data: BaseEmployeeSchema):
        """This method creates a new employee record in the database"""
        new_employee = employee_data.dict()

        async with db.begin():
            db.add(self.model(**new_employee))

        await db.commit()

    async def get_employee(self, db: AsyncSession, employee_id):
        """ This method retrieves a specific employee
        from the database based on their ID"""
        async with db.begin():
            query = select(self.model).filter(Employee.id == employee_id)
            result = await db.execute(query)
            employee = result.unique().scalars().first()
            return employee

    async def update_employee(
            self, db: AsyncSession, employee_id,
            employees_data: EmployeeCreateUpdateSchema):
        """ This method updates an existing employee record in the database"""
        async with db.begin():
            query = update(
                self.model).where(
                self.model.id == employee_id).values(employees_data.dict())
            await db.execute(query)
            await db.commit()

    async def delete_employee(self, db: AsyncSession, employee_id):
        """ This method deletes an employee record from the database"""
        async with db.begin():
            query = delete(self.model).where(self.model.id == employee_id)
            await db.execute(query)
            await db.commit()

    async def get_employees_busy(self, db: AsyncSession):
        """ This method retrieves all employees with active tasks"""
        employees_with_active_tasks = await (
            self.employee_dao.get_employees_busy(db))
        logged_employees = []
        for employee in employees_with_active_tasks:
            logged_employee = EmployeesSchema.model_validate(employee)
            logged_employees.append(logged_employee)
        return logged_employees

    async def find_least_loaded_employee(
            self, db: AsyncSession, task: TaskSchema
    ):
        """ This method retrieves the employee with the least loaded tasks"""
        employee = await self.model.employees_dao.find_least_loaded_employee(db, task)
        return EmployeesSchema.model_validate(employee)
