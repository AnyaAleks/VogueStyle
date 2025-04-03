from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import *
from os import getenv

DATABASE_URL = f"postgresql+asyncpg://{getenv('PGUSERNAME', 'admin')}:{getenv('PGPASSWORD', 'admin')}@db:5432/voguestyle"
engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session
        
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(MasterModel.metadata.create_all)
        await conn.run_sync(ServiceModel.metadata.create_all)
        await conn.run_sync(UserModel.metadata.create_all)
        await conn.run_sync(RequestModel.metadata.create_all)