from dao.tasks_dao import TaskDAO


class TaskService:

    def create_task(self, task_data):
        return self.task_dao.create_task(task_data)

    def get_task(self, task_id):
        return self.task_dao.get_task(task_id)

    def update_task(self, task_id, updated_data):
        return self.task_dao.update_task(task_id, updated_data)

    def delete_task(self, task_id):
        return self.task_dao.delete_task(task_id)

    def get_important_tasks(self):
        return self.task_dao.get_important_tasks()

    def __init__(self, task_dao: TaskDAO):
        self.task_dao = task_dao
