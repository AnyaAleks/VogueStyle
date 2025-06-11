from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models.base_model import Base

DATABASE_URL = f"postgresql+asyncpg://{getenv('PGUSERNAME', 'admin')}:{getenv('PGPASSWORD', 'admin')}@{getenv('PGIP', 'db')}:5432/voguestyle"
engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session
        
async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)