from fastapi import FastAPI

from routers import employees_router, tasks_router

app = FastAPI()
app.include_router(employees_router.employee_router)
app.include_router(tasks_router.task_router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)