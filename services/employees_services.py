from dao.employees_dao import EmployeeDAO


class EmployeeService:
    def __init__(self, employee_dao: EmployeeDAO):
        self.employee_dao = employee_dao

    def create_employee(self, employee_data):
        return self.employee_dao.create_employee(employee_data)

    def get_employee(self, employee_id):
        return self.employee_dao.get_employee(employee_id)

    def update_employee(self, employee_id, updated_data):
        return self.employee_dao.update_employee(employee_id, updated_data)

    def delete_employee(self, employee_id):
        return self.employee_dao.delete_employee(employee_id)

    def __init__(self, employee_dao: EmployeeDAO):
        self.employee_dao = employee_dao

    def get_busy_employees(self):
        return self.employee_dao.get_busy_employees()

