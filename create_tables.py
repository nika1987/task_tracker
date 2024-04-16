from asyncio import run

from dao import Base, engine
from utils import get_db


async def create_tables() -> None:
    """This function creates the tables in the data"""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    db = await get_db()
    await db.commit()
    await db.close()

run(create_tables())
