from sqlalchemy import select, update, delete, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dao.models import Employee, Task

from services.schemas import BaseEmployeeSchema, EmployeeCreateUpdateSchema


class EmployeeService:
    """The EmployeeDao class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the EmployeeDao class"""
        self.model = Employee
        self.tasks = Task

    async def get_all_employees(self, db: AsyncSession):
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            employees = result.scalars().all()
            return employees

    async def create_employee(self, db: AsyncSession, employee_data: BaseEmployeeSchema):
        """This method creates a new employee record in the database
        :param db: an instance of the AsyncSession provides a connection to the database
        :param employee_data: an instance of BaseEmployeesSchema containing data for the new employee
        :return: True if the employee was successfully created, False otherwise
        """
        new_employee = employee_data.dict()

        async with db.begin():
            db.add(self.model(**new_employee))

        await db.commit()

    async def get_employee(self, db: AsyncSession, employee_id):
        async with db.begin():
            query = select(self.model).filter(Employee.id == employee_id)
            result = await db.execute(query)
            employees = result.scalars().all()
            return employees

    async def update_employee(self, db: AsyncSession, employee_id, employees_data: EmployeeCreateUpdateSchema):
        # Реализация логики для обновления информации о сотруднике
        async with db.begin():
            query = update(self.model).where(self.model.id == employee_id).values(employees_data.dict())
            await db.execute(query)
            await db.commit()

    async def delete_employee(self, db: AsyncSession, employee_id):
        # Реализация логики для удаления сотрудника
        async with db.begin():
            query = delete(self.model).where(self.model.id == employee_id)
            await db.execute(query)
            await db.commit()

    async def get_employees_busy(self, db: AsyncSession):
        async with db.begin():
            query = (
                select(Employee).
                join(Task).
                filter(Task.tasks_status == Employee.positions).
                filter(Task.tasks_status == 'active').
                options(selectinload(Employee.tasks)).
                group_by(Employee.id).
                order_by(func.count(Task.id).desc())
            )
            await db.execute(query)
            await db.commit()


    async def find_least_loaded_employee(self, db: AsyncSession):
        # Поиск наименее загруженного сотрудника
        async with db.begin():
            pass
            query = select(self.model).filter(self.model.positions != 'busy')
            result = await db.execute(query)
            find_least_loaded_employee = result.scalars().all()
            return find_least_loaded_employee

    async def find_employee_for_task(self, db: AsyncSession):
        # Поиск сотрудника для выполнения важной задачи
        async with db.begin():
            pass
