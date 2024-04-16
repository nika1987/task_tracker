from fastapi import FastAPI, Depends
from services import schemas
from sqlalchemy.ext.asyncio import AsyncSession


from container import employees_service
from utils import get_db

app = FastAPI()


@app.get(
    '/employees/vacant', response_model=list[schemas.BaseEmployeeSchema],
    summary='Get a list of all available employees',
    description='This route returns all vacant employees')
async def get_all_employees(
        session: AsyncSession = Depends(get_db)
) -> list[schemas.EmployeesSchema]:
    """This view serves to receive all vacant tables
    :param session: an instance of AsyncSession providing by get_db function
    :return: a list of TableSchema instances
    """
    employees = await employees_service.get_all_employees(session)
    return employees


@app.get("/tasks")
def get_task():
    return
    pass


@app.get("/busy_employees")
def get_busy_employees():
    return
    pass


@app.get("/important_task")
def get_important_tasks():
    return
    pass
