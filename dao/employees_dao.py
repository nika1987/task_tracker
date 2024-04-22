from sqlalchemy import select, func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dao.models import Employee, Task

from services.schemas import BaseEmployeeSchema, EmployeeCreateUpdateSchema


class EmployeeDao:
    """The TableDao class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the TableDao class"""
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
            result = await db.execute(
                self.model.table.insert().values(new_employee)
            )
            return bool(result.rowcount)

    async def get_employee(self, db: AsyncSession, employee_id):
        async with db.begin():
            query = select(self.model).filter(Employee.id == employee_id)
            result = await db.execute(query)
            employee = result.scalars().first()
            return employee

    async def update_employee(self, db: AsyncSession, employee_id, employees_data: EmployeeCreateUpdateSchema):
        # Реализация логики для обновления информации о сотруднике
        async with db.begin():
            result = await db.execute(
                self.model.table.update()
                .where(self.model.id == employee_id)
                .values(employees_data.dict())
            )
            return bool(result.rowcount)

    async def delete_employee(self, db: AsyncSession, employee_id):
        # Реализация логики для удаления сотрудника
        async with db.begin():
            result = await db.execute(
                self.model.table.delete().where(self.model.id == employee_id)
            )
            return bool(result.rowcount)

    async def get_employees_busy(self, db: AsyncSession):
        async with db.begin():
            query = (
                select(Employee).
                join(Task).
                filter(self.tasks.status == self.model.employee_positions).
                filter(self.tasks.tasks_status == "active").
                options(selectinload(Employee.tasks)).
                group_by(Employee.id).
                order_by(func.count(Task.id).desc())
            )
            result = await db.execute(query)
            employees_with_active_tasks = result.scalars().all()
            return employees_with_active_tasks

    async def find_least_loaded_employee(self, db: AsyncSession):
        # Поиск наименее загруженного сотрудника
        async with db.begin():
            query = select(self.model).filter(self.model.positions != 'busy')
            result = await db.execute(query)
            find_least_loaded_employee = result.scalars().all()
            return find_least_loaded_employee

    async def find_employee_for_task(self, db: AsyncSession):
        # Поиск сотрудника для выполнения важной задачи
        async with db.begin():
            pass
            pass
