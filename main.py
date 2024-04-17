from fastapi import FastAPI

from routers import employees_router


app = FastAPI()
app.include_router(employees_router.employee_router)
