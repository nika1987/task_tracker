from dao.employees_dao import EmployeesDao


class EmployeesService:
    def __init__(self):
        self.employees_dao = EmployeesDao()

    async def create_employee(self, session, employee_data):
        created = await self.employees_dao.create_employee(session, employee_data)
        return created

    async def get_employee(self, session, employee_id):
        employee = await get_employee(session, employee_id)
        return employee

    async def update_employee(self, employee_id, employee_data):
        updated = await self.employees_dao.update_employee(employee_id, employee_data)
        return updated

    async def delete_employee(self, employee_id):
        deleted = await self.employees_dao.delete_employee(employee_id)
        return deleted

    async def get_busy_employees(self):
        busy_employees = await self.employees_dao.get_busy_employees
        return busy_employees
