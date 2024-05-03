from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.models import Task

from src.services.schemas import BaseTaskSchema, TaskCreateUpdateSchema


class TaskDAO:
    """Class for working with tasks data in the database"""
    def __init__(self):
        self.model = Task

    async def get_all_tasks(self, db: AsyncSession):
        """Retrieve all tasks from the database"""
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            tasks = result.scalars().all()
            return tasks

    async def create_task(self, db: AsyncSession, task_data: BaseTaskSchema):
        """Create new task in the database"""
        new_task = task_data.dict()
        async with db.begin():
            result = await db.execute(
                self.model.table.insert().values(new_task)
            )
            return bool(result.rowcount)

    async def get_task(self, db: AsyncSession, task_id):
        """Retrieve task from the database"""
        async with db.begin():
            query = select(self.model).filter(Task.id == task_id)
            result = await db.execute(query)
            task = result.scalars().first()
            return task

    async def update_task(
            self, task_id, db: AsyncSession,
            updated_data: TaskCreateUpdateSchema):
        """Update task from the database"""
        async with db.begin():
            result = await db.execute(
                self.model.table.update()
                .where(self.model.id == task_id)
                .values(updated_data.dict())
            )
            return bool(result.rowcount)

    async def delete_task(self, task_id, db: AsyncSession, ):
        """Delete task from the database"""
        async with db.begin():
            result = await db.execute(
                self.model.table.delete().where(self.model.id == task_id)
            )
        return bool(result.rowcount)

    async def get_important_tasks(self, db: AsyncSession):
        """Retrieve important tasks from the database"""
        async with db.begin():
            query = select(
                self.model).filter(
                self.model.status != 'active',
                self.model.parent_task_id is not None,
                self.model.parent_task.has(
                    self.model.status == 'active'
                )
            )

            result = await db.execute(query)
            important_tasks = result.unique().scalars().all()
            return important_tasks
