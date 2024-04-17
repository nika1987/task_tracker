from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dao.models import Task

from services.schemas import BaseTaskSchema, TaskCreateUpdateSchema


class TaskDAO:
    def __init__(self):
        self.model = Task

    async def get_all_tasks(self, db: AsyncSession):
        async with db.begin():
            query = select(self.model)
            result = await db.execute(query)
            tasks = result.scalars().all()
            return tasks

    async def create_task(self, db: AsyncSession, task_data: BaseTaskSchema):
        new_task = task_data.dict()
        async with db.begin():
            result = await db.execute(
                self.model.table.insert().values(new_task)
            )
            return bool(result.rowcount)

    async def get_task(self, db: AsyncSession, task_id):
        async with db.begin():
            query = select(self.model).filter(Task.id == task_id)
            result = await db.execute(query)
            task = result.scalars().first()
            return task

    async def update_task(self, task_id, db: AsyncSession, updated_data: TaskCreateUpdateSchema):
        async with db.begin():
            result = await db.execute(
                self.model.table.update()
                .where(self.model.id == task_id)
                .values(updated_data.dict())
            )
            return bool(result.rowcount)

    async def delete_task(self, task_id, db: AsyncSession, ):
        async with db.begin():
            result = await db.execute(
                self.model.table.delete().where(self.model.id == task_id)
            )
        return bool(result.rowcount)

    async def get_important_tasks(self, db: AsyncSession):
        async with db.begin():
            query = select(self.model).filter(self.model.important == True)
            result = await db.execute(query)
            important_tasks = result.scalars().all()
            return important_tasks

    async def get_unassigned_tasks(self, db: AsyncSession):
        # Запрос задач, которые не взяты в работу
        async with db.begin():
            query = select(self.model).filter(self.model.assigned_to is None)
            result = await db.execute(query)
            unassigned_tasks: Sequence[Task] = result.scalars().all()
            return unassigned_tasks

    async def get_dependent_tasks(self, db: AsyncSession):
        # Запрос задач, от которых зависят другие задачи
        async with db.begin():
            pass
            query = select(self.model).filter(self.model.depends_on != None)
            result = await db.execute(query)
            dependent_tasks = result.scalars().all()
            return dependent_tasks
