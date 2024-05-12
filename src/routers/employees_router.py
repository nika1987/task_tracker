from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.container import employees_service, tasks_service

from src.services.schemas import (
    EmployeeCreateUpdateSchema,
    EmployeeUpdateSchema)
from src.utils import get_db

employee_router = APIRouter(tags=['employees'], prefix='/employees')


@employee_router.post('/create', status_code=201)
async def create_employee_router(
        data: EmployeeCreateUpdateSchema, db: AsyncSession = Depends(get_db)
):
    return await employees_service.create_employee(db, data)


@employee_router.get('/list')
async def employees_list_router(
        db: AsyncSession = Depends(get_db)
):
    all_employees = await employees_service.get_all_employees(db)
    if not all_employees:
        raise HTTPException(status_code=404, detail="Employees not found")
    return all_employees


@employee_router.get('/busy', status_code=200)
async def get_busy_employees(db: AsyncSession = Depends(get_db)):
    busy_employees = await employees_service.get_employees_busy(db)
    if not busy_employees:
        raise HTTPException(
            status_code=404, detail="You have no busy employees"
        )
    return busy_employees


@employee_router.get('/free', status_code=200)
async def get_free_employees(db: AsyncSession = Depends(get_db)):
    important_tasks = await tasks_service.get_important_tasks(db)
    if not important_tasks:
        raise HTTPException(
            status_code=404,
            detail="You have no important tasks to find an employee"
        )
    less_busy_employees = []
    for task in important_tasks:
        found_employee = await employees_service.find_least_loaded_employee(
            db, task)
        less_busy_employees.append(
            {'task': task, 'employee': found_employee.name})

    if not less_busy_employees:
        raise HTTPException(
            status_code=404, detail="You have no free employees"
        )
    return less_busy_employees


@employee_router.get('/{employee_id}')
async def single_employee_router(
        employee_id: int, db: AsyncSession = Depends(get_db)
):
    found_employee = await employees_service.get_employee(db, employee_id)
    if not found_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return found_employee


@employee_router.put('/update', status_code=200)
async def update_employee_router(
        employee_id: int, data: EmployeeUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    return await employees_service.update_employee(db, employee_id, data)


@employee_router.delete('/delete', status_code=204)
async def delete_employee_router(
        employee_id: int, db: AsyncSession = Depends(get_db)
):
    return await employees_service.delete_employee(db, employee_id)

