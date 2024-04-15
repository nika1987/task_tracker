from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

# Устанавливаем соединение с бд
conn = psycopg2.connect(
    dbname="treker_task",
    user="user",
    password="postgres",
    host=5342
)


@app.get("/employees")
def get_employees():
    return
    pass


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