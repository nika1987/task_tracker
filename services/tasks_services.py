from dao.tasks_dao import TaskDAO
from services.schemas import BaseTaskSchema


class TaskService:
    def __init__(self, task_dao: TaskDAO):
        self.task_dao = task_dao

    def create_task(self, task_data: BaseTaskSchema):
        return self.task_dao.create_task(task_data)

    async def get_task(self, task_id):
        return await self.task_dao.get_task(task_id)

    async def get_important_tasks(self):
        unassigned_tasks = await self.task_dao.get_unassigned_tasks()
        dependent_tasks = await self.task_dao.get_dependent_tasks()

        # Логика поиска подходящих сотрудников
        least_loaded_employee = await self.task_dao.find_least_loaded_employee()

        # Возвращает список объектов [{Важная задача, Срок, [ФИО сотрудника]}]
        #return important_tasks
