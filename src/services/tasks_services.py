from pydantic import ValidationError
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.employees_dao import Employee
from src.dao.tasks_dao import Task

from src.services.schemas import (BaseTaskSchema,
                                  TaskCreateUpdateSchema, TaskSchema)


class TaskService:
    """The TaskService class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the TaskDao class"""

        self.model = Task
        self.employees = Employee

    async def get_all_tasks(self, db: AsyncSession):
        """ This method retrieves all tasks from the database"""
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            tasks = result.scalars().all()
            return tasks

    async def create_task(self, db: AsyncSession, task_data: BaseTaskSchema):
        """ This method creates a new task record in the database"""
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
        """ This method retrieves a specific task
        from the database based on their ID"""
        async with db.begin():
            query = select(self.model).filter(Task.id == task_id)
            result = await db.execute(query)
            task = result.scalars().first()
            return task

    async def update_task(
            self, db: AsyncSession, task_id,
            task_data: TaskCreateUpdateSchema):
        """ This method updates an existing task
        record in the database"""
        async with db.begin():
            query = update(
                self.model).where(
                self.model.id == task_id).values(task_data.dict())
            await db.execute(query)
            await db.commit()

    async def delete_task(self, db: AsyncSession, task_id):
        """ This method deletes an task record from the database"""
        async with db.begin():
            query = delete(self.model).where(self.model.id == task_id)
            await db.execute(query)
            await db.commit()

    async def get_important_tasks(self, db: AsyncSession):
        """ This method retrieves important tasks from the database"""
        important_tasks = await self.task_dao.get_important_tasks(db)
        return [TaskSchema.model_validate(task) for task in important_tasks]
