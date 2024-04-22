from sqlalchemy import select, func, desc, asc

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from dao.models import Employee, Task

from services.schemas import BaseEmployeeSchema, EmployeeCreateUpdateSchema, EmployeesSchema, TaskSchema


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

    async def get_employees_busy(self, db: AsyncSession) -> list:
        async with (db.begin()):
            query = select(
                self.model, func.count(self.tasks.id).label('tasks_count')
            ).join(self.tasks).filter(
                self.tasks.status == 'active'
            ).group_by(self.model).order_by(
                desc('tasks_count')
            )

            result = await db.execute(query)
            employees_with_active_tasks = result.scalars().all()

        return employees_with_active_tasks

    async def find_least_loaded_employee(
            self, db: AsyncSession, task: TaskSchema
    ):
        # Поиск наименее загруженного сотрудника
        async with db.begin():
            free_employee_query = select(self.model).filter(
                self.model.tasks == None
            )
            result = await db.execute(free_employee_query)
            free_employee = result.unique().scalars().first()
            less_loaded_employee_query = select(
                self.model, count(self.model.tasks).label('count')
            ).join(self.model.tasks).group_by(self.model.id).order_by(
                asc('count')
            )
            result = await db.execute(less_loaded_employee_query)
            least_loaded_employee = result.unique().scalars().first()
            optimal_employee_query = select(
                self.model

            ).join(self.model.tasks).filter(
                self.model.tasks.any(
                    parent_task_id=task.parent_task_id, status='active')
            ).group_by(self.model).having(
                count(self.model.tasks) <= len(least_loaded_employee.tasks)
            )

            result = await db.execute(optimal_employee_query)
            optimal_employee = result.unique().scalars().first()

            return optimal_employee or free_employee or least_loaded_employee
