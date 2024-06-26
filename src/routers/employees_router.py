from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.container import employees_service, tasks_service

from src.services.schemas import (
    EmployeeCreateUpdateSchema,
    EmployeeUpdateSchema)
from src.utils import get_db
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

employee_router = APIRouter(tags=['employees'], prefix='/employees')


@employee_router.post('/create', status_code=201)
async def create_employee_router(
        data: EmployeeCreateUpdateSchema, db: AsyncSession = Depends(get_db)
):
    try:
        return await employees_service.create_employee(db, data)
    except IntegrityError:
        return JSONResponse(
            status_code=400, content={'message': 'Ошибка при создании работника'}
        )


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
        return JSONResponse({'detail': "All employees are free"}, 200)
    return busy_employees


@employee_router.get('/free', status_code=200)
async def get_free_employees(db: AsyncSession = Depends(get_db)):
    important_tasks = await tasks_service.get_important_tasks(db)
    free_employees = [employee for employee in important_tasks if not employee.is_important]
    important_tasks = await tasks_service.get_important_tasks(db)

    employees_with_tasks = [task.employee_id for task in important_tasks]

    free_employees_without_important_tasks = []
    for employee in free_employees:
        if employee.id not in employees_with_tasks:
            free_employees_without_important_tasks.append(employee)

    return free_employees_without_important_tasks


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
    updated_employee = await employees_service.update_employee(db, employee_id, data)

    if updated_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return updated_employee


@employee_router.delete('/delete', status_code=204)
async def delete_employee_router(
        employee_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        found_employee = await employees_service.get_employee(db, employee_id)
        if not found_employee:
            raise HTTPException(status_code=404, detail="Работника с указанным ID не существует")
        else:
            await employees_service.delete_employee(db, employee_id)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Работник не может быть удален"
        )
