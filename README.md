## Description
This is a server application built with FastAPI for managing a Postgres database representing a task tracker. The application allows for managing data about employees and tasks, as well as finding the least busy employees for new tasks.

## Installation
README for Flask API:

# Project Setup

1. Install all necessary dependencies by running the command:
      pip install -r requirements.txt
2. Create an environment variables file named .env and specify the required environment variables.
3. Start Docker Compose to run the database and other services:
      docker-compose up
4. Create a database migration using Alembic:
      alembic revision --autogenerate -m "Migration Name"
5. Run the server:
 uvicorn main:app --reload




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
