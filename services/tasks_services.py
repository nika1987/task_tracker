from dao.tasks_dao import TaskDAO
from services.shemas import BaseTasksSchema, TaskChangeSchema


class TaskService:
    def __init__(self, task_dao: TaskDAO):
        self.task_dao = task_dao

    def create_task(self, task_data: BaseTasksSchema):
        return self.task_dao.create_task(task_data)

    async def get_task(self, task_id):
        return await self.task_dao.get_task(task_id)

    async def update_task(self, task_id, updated_data: TaskChangeSchema):
        return await self.task_dao.update_task(task_id, updated_data)

    async def delete_task(self, task_id):
        return await self.task_dao.delete_task(task_id)

    async def get_important_tasks(self):
        return await self.task_dao.get_important_tasks()

