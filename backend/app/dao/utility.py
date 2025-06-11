from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_object_by_id(model, object_id: int, session: AsyncSession):
    result = await session.execute(select(model).where(model.id == object_id))
    return result.scalar_one_or_none()