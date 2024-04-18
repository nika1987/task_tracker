from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from container import employees_service

from services.schemas import EmployeeCreateUpdateSchema
from utils import get_db

employee_router = APIRouter(tags=['employees'], prefix='/employees')


@employee_router.post('/create')
async def create_employee_router(
        data: EmployeeCreateUpdateSchema, db: AsyncSession = Depends(get_db)
):
    await employees_service.create_employee(db, data)


@employee_router.get('/list')
async def employees_list_router(
        db: AsyncSession = Depends(get_db)
):
    all_employees = await employees_service.get_all_employees(db)
    return all_employees


@employee_router.get('/{employee_id}')
async def single_employee_router(
        employee_id: int, db: AsyncSession = Depends(get_db)
):
    return await employees_service.get_employee(db, employee_id)


@employee_router.put('/update')
async def update_employee_router(
        employee_id: int,
        data: EmployeeCreateUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    await employees_service.update_employee(db, employee_id, data)


@employee_router.delete('/delete')
async def update_employee_router(
        employee_id: int, db: AsyncSession = Depends(get_db)
):
    await employees_service.delete_employee(db, employee_id)
