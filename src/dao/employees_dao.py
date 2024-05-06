from typing import Any, Sequence

from sqlalchemy import select, func, desc, asc, Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.sql.functions import count

from src.dao.models import Employee, Task

from ..services.schemas import (
    BaseEmployeeSchema, EmployeeCreateUpdateSchema, TaskSchema)


class EmployeeDao:
    """The EmployeeDao class provides access to the employees table"""

    def __init__(self) -> None:
        """Initialize the EmployeeDao class"""
        self.model = Employee
        self.tasks = Task

    async def get_all_employees(self, db: AsyncSession):
        """Retrieve all employees from the database."""
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            employees = result.scalars().all()
            return employees

    async def create_employee(
            self, db: AsyncSession, employee_data: BaseEmployeeSchema):
        """Create a new employee record in the database"""
        new_employee = employee_data.dict()

        async with db.begin():
            result = await db.execute(
                self.model.table.insert().values(new_employee)
            )
            return bool(result.rowcount)

    async def get_employee(self, db: AsyncSession, employee_id):
        """Retrieve a specific employee from the database based on their ID."""
        async with db.begin():
            query = select(self.model).filter(Employee.id == employee_id)
            result = await db.execute(query)
            employee = result.scalars().first()
            return employee

    async def update_employee(
            self, db: AsyncSession, employee_id,
            employees_data: EmployeeCreateUpdateSchema):
        """Update an existing employee record in the database."""
        async with db.begin():
            result = await db.execute(
                self.model.table.update()
                .where(self.model.id == employee_id)
                .values(employees_data.dict())
            )
            return bool(result.rowcount)

    async def delete_employee(self, db: AsyncSession, employee_id):
        """Delete an employee record from the database."""
        async with db.begin():
            result = await db.execute(
                self.model.table.delete().where(self.model.id == employee_id)
            )
            return bool(result.rowcount)

    async def get_employees_busy(self, db: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
        """Retrieve employees with active tasks from the database """
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
        """Find the employee with the least loaded tasks"""

        async with db.begin():
            free_employee_query = select(self.model).filter(
                self.model.tasks is None
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
