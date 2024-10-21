


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager

Base = declarative_base()

# Database URL for asynchronous connection (using asyncpg as a driver)
DATABASE_URL = "postgresql+asyncpg://Your database"

# Create an asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker factory for generating database sessions
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)


# Asynchronous function to create all tables
async def create_tables():
    async with engine.begin() as conn:
        # Recreate the table with the updated schema
        await conn.run_sync(Base.metadata.create_all)

# Dependency function to provide a session per request
async def get_db():
    async with async_session() as session:
        yield session

