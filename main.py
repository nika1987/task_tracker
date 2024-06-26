from fastapi import FastAPI

from src.routers import employees_router
from src.routers import tasks_router

app: FastAPI = FastAPI()

app.include_router(tasks_router.task_router)
app.include_router(employees_router.employee_router)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8005, reload=True)
