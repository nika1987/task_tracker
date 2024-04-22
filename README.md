#Task Tracker Server

## Description
This is a server application built with FastAPI for managing a Postgres database representing a task tracker. The application allows for managing data about employees and tasks, as well as finding the least busy employees for new tasks.

## Installation
1. Install dependencies:
pip install fastapi
pip install uvicorn
pip install psycopg2

2. Create a Postgres database and import the schema from the schema.sql file.

3. Run the server:
uvicorn main:app –reload

## Technologies used in the project:

Fastapi
SQLAlchemy
Uvicorn
Bcrypt
PyJwt
Docker
Docker-compose

## Usage
1. API documentation is available at http://localhost:8000/docs.

## Author
Veronika Zolotova