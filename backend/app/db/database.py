from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


DATABASE_FILENAME = "database.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_FILENAME}"

engine = create_async_engine(
    DATABASE_URL, echo=False)


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:

    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
