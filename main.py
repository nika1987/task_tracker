from fastapi import FastAPI

from routers import employees_router, tasks_router

app = FastAPI()
app.include_router(employees_router.employee_router)
app.include_router(tasks_router.task_router)
