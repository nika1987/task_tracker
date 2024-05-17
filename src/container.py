from task_tracker.src.services.employees_services import EmployeeService
from task_tracker.src.services.tasks_services import TaskService
from task_tracker.src.dao.employees_dao import EmployeeDao
from task_tracker.src.dao.tasks_dao import TaskDAO

task_dao = TaskDAO()
employee_dao = EmployeeDao()
employees_service = EmployeeService()
tasks_service = TaskService()
