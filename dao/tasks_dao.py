import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_session
from sqlalchemy.testing import db

from dao.models import Tasks

from services.shemas import TaskChangeSchema, BaseTasksSchema


class TaskDAO:
    def __init__(self):
        self.model = None

    def init(self):
        self.model = Tasks

    async def create_task(self, task_data: BaseTasksSchema):
        new_task = {
            "title": task_data.title,
            "description": task_data.description,
            "status": task_data.status
        }
        async with db.begin():
            result = await db.execute(
                self.model.table.insert().values(new_task)
            )
            return bool(result.rowcount)

    async def get_task(self, task_id):
        async with self as session:
            query = select(Tasks).filter(Tasks.id == task_id)
            result = await session.execute(query)
            employee = result.scalars().first()
            return employee

    @staticmethod
    async def update_task(task_id, updated_data: TaskChangeSchema):
        await asyncio.sleep(1)
        updated_data.promote_task('New Task')
        updated_data.delete_task_fields()
        return f"Task {task_id} updated with data: {updated_data.dict()}"

    @staticmethod
    async def delete_task(task_id):
        await asyncio.sleep(1)
        return f"Task {task_id} deleted"

    @property
    async def get_important_tasks(self):
        DATABASE_URL: str = "postgresql+asyncpg://username:password@localhost/dbname"
        engine = create_async_engine(DATABASE_URL, echo=True)

        async with async_session(engine) as session:
            stmt = select(Tasks).filter(Tasks.positions == 'busy')
            result = await session.execute(stmt)
            busy_employees = [employee.name for employee in result.scalars()]

            return busy_employees
