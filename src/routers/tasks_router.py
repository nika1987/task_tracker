from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.container import tasks_service
from src.services.schemas import TaskCreateUpdateSchema
from src.utils import get_db

task_router = APIRouter(tags=['tasks'], prefix='/tasks')


@task_router.post('/create')
async def create_task_router(
        data: TaskCreateUpdateSchema, db: AsyncSession = Depends(get_db)
):
    await tasks_service.create_task(db, data)


@task_router.get('/list')
async def tasks_list_router(
        db: AsyncSession = Depends(get_db)
):
    all_tasks = await tasks_service.get_all_tasks(db)
    return all_tasks


@task_router.get('/important')
async def important_tasks_list_router(
        db: AsyncSession = Depends(get_db)
):
    all_tasks = await tasks_service.get_important_tasks(db)
    return all_tasks


@task_router.get('/{task_id}')
async def single_task_router(
        task_id: int, db: AsyncSession = Depends(get_db)
):
    return await tasks_service.get_task(db, task_id)


@task_router.put('/update')
async def update_task_router(
        task_id: int,
        data: TaskCreateUpdateSchema,
        db: AsyncSession = Depends(get_db)
):
    await tasks_service.update_task(db, task_id, data)


@task_router.delete('/delete')
async def update_task_router(
        task_id: int, db: AsyncSession = Depends(get_db)
):
    await tasks_service.delete_task(db, task_id)
