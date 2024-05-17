"""This file contains a different database objects to create db models and
provides connection to the database"""
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from task_tracker.src.constans import DB_URI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
# --------------------------------------------------------------------------

engine = create_async_engine(DB_URI)

SessionLocal: sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
