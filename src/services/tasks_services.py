from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from task_tracker.src.dao.employees_dao import Employee
from task_tracker.src.dao.tasks_dao import Task, TaskDAO
from task_tracker.src.services.schemas import (
    BaseTaskSchema,
    TaskUpdateSchema)


class TaskService:
    """The TaskService class provides access to the table spreadsheet"""

    def __init__(self) -> None:
        """Initialize the TaskDao class"""

        self.task_dao = TaskDAO()
        self.model = Task
        self.employees = Employee

    async def get_all_tasks(self, db: AsyncSession):
        """ This method retrieves all tasks from the database"""
        try:
            tasks = await self.task_dao.get_all_tasks(db)
            return tasks
        except Exception as e:
            print(f'Can not get tasks: {e}')
            return []

    async def create_task(self, db: AsyncSession, task_data: BaseTaskSchema):
        """ This method creates a new task record in the database"""
        try:
            new_task = await self.task_dao.create_task(db, task_data)
            return new_task
        except ValidationError as e:
            # Если данные не прошли валидацию, обработайте ошибку здесь
            print(f"Ошибка валидации данных: {e}")
            raise HTTPException(
                status_code=400, detail=f'Can not create task: {e}'
            )

    async def get_task(self, db: AsyncSession, task_id):
        """ This method retrieves a specific task
        from the database based on their ID"""
        try:
            task = await self.task_dao.get_task(db, task_id)
            return task
        except Exception as e:
            print(f'Can not get task: {e}')
            return None

    async def update_task(
            self, db: AsyncSession, task_id,
            task_data: TaskUpdateSchema):
        """ This method updates an existing task
        record in the database"""
        try:
            updated_task = await self.task_dao.update_task(
                task_id, db, task_data
            )
            return updated_task
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f'Can not update task: {e}'
            )

    async def delete_task(self, db: AsyncSession, task_id):
        """ This method deletes a task record from the database"""
        try:
            await self.task_dao.delete_task(db, task_id)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f'Can not delete task: {e}'
            )

    async def get_important_tasks(self, db: AsyncSession):
        """This method retrieves all important tasks from the database"""
        important_tasks = await self.task_dao.get_important_tasks(db)
        return important_tasks
