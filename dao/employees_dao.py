import asyncio

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_session

from dao.models import Employees, Tasks
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import Any

from services.shemas import EmployeesChangeSchema, BaseEmployeesSchema


class EmployeesDao:
    """The TableDao class provides access to the table spreadsheet"""

    def init(self) -> None:
        """Initialize the TableDao class"""
        self.model = Employees
        self.tasks = Tasks

    async def create_employee(self, db: AsyncSession, employee_data: BaseEmployeesSchema):
        """This method creates a new employee record in the database
        :param db: an instance of the AsyncSession provides a connection to the database
        :param employee_data: an instance of BaseEmployeesSchema containing data for the new employee
        :return: True if the employee was successfully created, False otherwise
        """
        new_employee = {
            'name': employee_data.name,
            'position': employee_data.positions,
            'department': employee_data.department,
            # Другие данные о сотруднике
        }

        async with db.begin():
            result = await db.execute(
                self.model.table.insert().values(new_employee)
            )
            return bool(result.rowcount)

    async def get_employee(self, employee_id):
        async with self as session:
            query = select(Employees).filter(Employees.id == employee_id)
            result = await session.execute(query)
            employee = result.scalars().first()
            return employee

    @staticmethod
    async def update_employee(employee_id, employees_data: EmployeesChangeSchema):
        # Реализация логики для обновления информации о сотруднике
        await asyncio.sleep(1)  # Пример асинхронной операции
        employees_data.promote_employee('New Position')
        employees_data.delete_employee()
        return f"Employee {employee_id} updated with data: {employees_data.dict()}"

    @staticmethod
    async def delete_employee(employee_id):
        # Реализация логики для удаления сотрудника
        await asyncio.sleep(1)  # Пример асинхронной операции
        return f"Employee {employee_id} deleted"

    @property
    async def get_busy_employees(self):
        # Обновите строку подключения к вашей базе данных PostgreSQL
        DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"

        engine = create_async_engine(DATABASE_URL, echo=True)

        async with async_session(engine) as session:
            stmt = select(Employees).filter(Employees.positions == 'busy')
            result = await session.execute(stmt)
            busy_employees = [employee.name for employee in result.scalars()]

        return busy_employees
