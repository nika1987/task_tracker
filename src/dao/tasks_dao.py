from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from task_tracker.src.dao.models import Task
from task_tracker.src.services.schemas import BaseTaskSchema, TaskUpdateSchema


class TaskDAO:
    """Class for working with tasks data in the database"""

    def __init__(self):
        self.model = Task

    async def get_all_tasks(self, db: AsyncSession):
        """Retrieve all tasks from the database"""
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            tasks = result.unique().scalars().all()
            return tasks

    async def create_task(self, db: AsyncSession, task_data: BaseTaskSchema):
        """Create new task in the database"""
        new_task = task_data.dict()
        async with db.begin():
            result = await db.execute(
                insert(self.model).values(new_task)
            )
            await db.commit()
        return await self.get_task(db, result.inserted_primary_key[0])

    async def get_task(self, db: AsyncSession, task_id):
        """Retrieve task from the database"""
        async with db.begin():
            query = select(self.model).filter(Task.id == task_id)
            result = await db.execute(query)
            task = result.unique().scalars().first()
            return task

    async def update_task(
            self, task_id, db: AsyncSession, updated_data: TaskUpdateSchema):
        """Update task from the database"""
        async with db.begin():
            query = update(
                self.model).where(
                self.model.id == task_id).values(
                updated_data.model_dump(exclude_unset=True))
            await db.execute(query)
            await db.commit()
        return await self.get_task(db, task_id)

    async def delete_task(self, task_id, db: AsyncSession, ):
        """Delete task from the database"""
        async with db.begin():
            query = delete(self.model).where(self.model.id == task_id)
            await db.execute(query)
            await db.commit()

    async def get_important_tasks(self, db: AsyncSession):
        """Retrieve important tasks from the database"""
        try:
            async with db.begin():
                query = select(
                    self.model).filter(
                    self.model.status != 'active',
                    self.model.urgency >= 4,
                    self.model.parent_task_id is not None,
                    self.model.parent_task.has(
                        self.model.status == 'active'
                    )
                )
            result = await db.execute(query)
            important_tasks = result.unique().scalars().all()
            return important_tasks
        except Exception as e:
            print(f"Произошла ошибка 500: {e}")
            return []
