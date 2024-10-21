# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# URL_DB = 'postgresql://postgres:SPM#2003@localhost/Email'

# engine = create_engine(URL_DB)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()




# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# DATABASE_URL = "postgresql+asyncpg://postgres:SPM#2003@localhost/Email"

# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(bind=engine, expire_on_commit=False)

# Base = declarative_base()

# async def create_tables():
#     async with engine.begin() as conn:
#         # Drop all tables if needed
#         # await conn.run_sync(Base.metadata.drop_all)
        
#         # Create all tables
#         await conn.run_sync(Base.metadata.create_all)

# # Dependency
# async def get_db():
#     async with async_session() as db:
#         yield db

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql+asyncpg://postgres:SPM#2003@localhost/Email"

# engine = create_async_engine(DATABASE_URL, echo=True)

# async_session = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False
# )

# Base = declarative_base()

# async def get_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#############################################______________TRACKING MAIL LINK_______________________________#######################
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base

# # Asynchronous connection string
# DATABASE_URL = "postgresql+asyncpg://postgres:SPM#2003@localhost/Email"


# Base=declarative_base()
# # Asynchronous engine for normal operation
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# # Asynchronous function to create all tables
# async def create_tables():
#     async with engine.begin() as conn:
#         # Recreate the table with the updated schema
#         await conn.run_sync(Base.metadata.create_all)



# async def get_db():
#     async with async_session() as session:
#         yield session

########################################____________________________________________tracking link and email status__________________________________________________###################################################

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # Database URL for asynchronous connection (using asyncpg as a driver)
# DATABASE_URL = "postgresql+asyncpg://postgres:SPM#2003@localhost/Email"

# # Create an asynchronous engine
# engine = create_async_engine(DATABASE_URL, echo=True)

# # Create a sessionmaker factory for generating database sessions
# async_session = sessionmaker(
#     bind=engine,
#     class_=AsyncSession,
#     autoflush=False,
#     expire_on_commit=False
# )


# # Asynchronous function to create all tables
# async def create_tables():
#     async with engine.begin() as conn:
#         # Recreate the table with the updated schema
#         await conn.run_sync(Base.metadata.create_all)


# # Dependency function to provide a session per request
# async def get_db():
#     async with async_session() as session:
#         yield session





####################################################################################################################################################################################









from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager

Base = declarative_base()

# Database URL for asynchronous connection (using asyncpg as a driver)
DATABASE_URL = "postgresql+asyncpg://postgres:SPM#2003@localhost/Email"

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




# # Dependency to get the database session
# @asynccontextmanager
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#             await session.commit()
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()

# @app.get("/users")
# async def get_users(db: AsyncSession = Depends(get_db)):
#     # Use the session for database operations
#     result = await db.execute("SELECT * FROM users")
#     users = result.fetchall()
#     return users



