from sqlalchemy.ext.asyncio import AsyncSession

from task_tracker.src.dao import SessionLocal


async def get_db() -> AsyncSession:
    """" This function returns a database session
    : return: AsyncSession instance
    """
    async with SessionLocal() as db:
        yield db
