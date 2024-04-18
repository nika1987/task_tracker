from pydantic import ValidationError
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from dao.models import Task, Employee

from services.schemas import BaseTaskSchema, TaskCreateUpdateSchema


class TaskService:
    """The TaskService class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the TaskDao class"""

        self.model = Task
        self.employees = Employee

    async def get_all_tasks(self, db: AsyncSession):
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            tasks = result.scalars().all()
            return tasks

    async def create_task(self, db: AsyncSession, task_data: BaseTaskSchema):
        try:
            validated_data = BaseTaskSchema(**task_data.dict())
            new_task = validated_data.dict()
            async with db.begin():
                db.add(self.model(**new_task))
            await db.commit()
        except ValidationError as e:
            # Если данные не прошли валидацию, обработайте ошибку здесь
            print(f"Ошибка валидации данных: {e}")

    async def get_task(self, db: AsyncSession, task_id):
        async with db.begin():
            query = select(self.model).filter(Task.id == task_id)
            result = await db.execute(query)
            task = result.scalars().first()
            return task

    async def update_task(self, db: AsyncSession, task_id, task_data: TaskCreateUpdateSchema):
        async with db.begin():
            query = update(self.model).where(self.model.id == task_id).values(task_data.dict())
            await db.execute(query)
            await db.commit()

    async def delete_task(self, db: AsyncSession, task_id):
        async with db.begin():
            query = delete(self.model).where(self.model.id == task_id)
            await db.execute(query)
            await db.commit()

    # async def get_important_tasks(self):
    # unassigned_tasks = await self.task_dao.get_unassigned_tasks()
    # dependent_tasks = await self.task_dao.get_dependent_tasks()

    # Логика поиска подходящих сотрудников
    # least_loaded_employee = await self.task_dao.find_least_loaded_employee()

    # Возвращает список объектов [{Важная задача, Срок, [ФИО сотрудника]}]
    # return important_tasks
