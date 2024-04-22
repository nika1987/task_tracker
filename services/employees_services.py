from sqlalchemy import select, update, delete, func, desc

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dao.models import Employee, Task

from services.schemas import BaseEmployeeSchema, EmployeeCreateUpdateSchema, EmployeesSchema, TaskSchema


class EmployeeService:
    """The EmployeeDao class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the EmployeeDao class"""
        self.model = Employee
        self.tasks = Task

    async def get_all_employees(self, db: AsyncSession):
        """This method retrieves all employees from the database"""
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            employees = result.scalars().all()
            return employees

    async def create_employee(self, db: AsyncSession, employee_data: BaseEmployeeSchema):
        """This method creates a new employee record in the database"""
        new_employee = employee_data.dict()

        async with db.begin():
            db.add(self.model(**new_employee))

        await db.commit()

    async def get_employee(self, db: AsyncSession, employee_id):
        """ This method retrieves a specific employee from the database based on their ID"""
        async with db.begin():
            query = select(self.model).filter(Employee.id == employee_id)
            result = await db.execute(query)
            employees = result.scalars().all()
            return employees

    async def update_employee(self, db: AsyncSession, employee_id, employees_data: EmployeeCreateUpdateSchema):
        """ This method updates an existing employee record in the database"""
        # Реализация логики для обновления информации о сотруднике
        async with db.begin():
            query = update(self.model).where(self.model.id == employee_id).values(employees_data.dict())
            await db.execute(query)
            await db.commit()

    async def delete_employee(self, db: AsyncSession, employee_id):
        """ This method deletes an employee record from the database"""
        # Реализация логики для удаления сотрудника
        async with db.begin():
            query = delete(self.model).where(self.model.id == employee_id)
            await db.execute(query)
            await db.commit()

    async def get_employees_busy(self, db: AsyncSession):
        """ This method retrieves a list of employees with active tasks"""
        # Реализация логики для получения списка сотрудников с активными задачами
        async with db.begin():
            query = select((self.model, func.count(self.tasks.id).label('task_count'))).join(self.tasks).filter(
                self.tasks.status == 'active').group_by(self.model).order_by(
                desc('task_count')
            )
            result = await db.execute(query)
            employees_with_active_tasks = result.scalars().all()
            return employees_with_active_tasks

    async def get_employees_busy(self, db: AsyncSession):
        """ This method retrieves a list of employees with active tasks"""
        employees_with_active_tasks = await (
            self.employee_dao.get_employees_busy(db))
        return [EmployeesSchema.model_validate(employee)
                for employee in employees_with_active_tasks]

    async def find_least_loaded_employee(
        self, db: AsyncSession, task: TaskSchema
    ):
        """ This method retrieves the employee with the least loaded tasks"""
        employee = await self.employee_dao.find_least_loaded_employee(db, task)
        return EmployeesSchema.model_validate(employee)
