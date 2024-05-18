from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.container import tasks_service
from src.services.schemas import TaskCreateUpdateSchema, TaskUpdateSchema
from src.utils import get_db

task_router = APIRouter(tags=['tasks'], prefix='/tasks')


@task_router.post('/create', status_code=201)
async def create_task_router(
        data: TaskCreateUpdateSchema, db: AsyncSession = Depends(get_db)
):
    return await tasks_service.create_task(db, data)


@task_router.get('/list')
async def tasks_list_router(
        db: AsyncSession = Depends(get_db)
):
    all_tasks = await tasks_service.get_all_tasks(db)
    if not all_tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return all_tasks


@task_router.get('/important', status_code=200)
async def important_tasks_list_router(
        db: AsyncSession = Depends(get_db)
):
    important_tasks = await tasks_service.get_important_tasks(db)
    if not important_tasks:
        raise HTTPException(
            status_code=404,
            detail="You have no important tasks"
        )
    return important_tasks


@task_router.get('/{task_id}')
async def single_task_router(
        task_id: int, db: AsyncSession = Depends(get_db)
):
    task = await tasks_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@task_router.put('/update', status_code=200)
async def update_task_router(
        task_id: int,
        data: TaskUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    updated_task = await tasks_service.update_task(db, task_id, data)

    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@task_router.delete('/delete', status_code=204)
async def delete_task_router(
        task_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        found_task = await tasks_service.get_task(db, task_id)
        if not found_task:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            await tasks_service.delete_task(db, task_id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Can not delete task")
