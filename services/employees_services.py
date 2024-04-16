
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from dao.employees_dao import EmployeeDao

from services.schemas import EmployeesSchema


class EmployeesService:
    def __init__(self, dao: EmployeeDao = EmployeeDao()) -> None:
        self.dao = dao
        self.employees_schema = EmployeesSchema

    async def get_all_employees(self, db: AsyncSession):
        employees = await self.dao.get_all_employees(db)
        if not employees:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Cannot find vacant tables')

        return employees
    #async def get_employee(self, session, employee_id):
        #employee = await get_employees(session, employee_id)
        #return employee

    async def update_employee(self, employee_id, employee_data):
        updated = await self.dao.update_employee(employee_id, employee_data)
        return updated

    async def delete_employee(self, employee_id):
        deleted = await self.employees_dao.delete_employee(employee_id)
        return deleted

    async def get_busy_employees(self):
        busy_employees = await self.employees_dao.get_busy_employees
        return busy_employees
