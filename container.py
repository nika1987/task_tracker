from services.employees_services import EmployeesService
from services.tasks_services import TaskService
from dao.employees_dao import EmployeeDao
from dao.tasks_dao import TaskDAO

task_dao = TaskDAO()
employee_dao = EmployeeDao()
employees_service = EmployeesService(employee_dao)
tasks_service = TaskService(task_dao)
