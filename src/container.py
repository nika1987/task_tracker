from src.services.employees_services import EmployeeService
from src.services.tasks_services import TaskService
from src.dao.employees_dao import EmployeeDao
from src.dao.tasks_dao import TaskDAO

task_dao = TaskDAO()
employee_dao = EmployeeDao()
employees_service = EmployeeService()
tasks_service = TaskService()
