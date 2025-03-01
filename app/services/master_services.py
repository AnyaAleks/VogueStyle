from sqlalchemy.ext.asyncio import AsyncSession
from schema.master_schema import MasterSchemaCreate
from models.master_model import MasterModel

async def _create_master(MasterInfo: MasterSchemaCreate, session: AsyncSession):
    master = MasterModel(
        fullname = MasterInfo.fullname,
        phone = MasterInfo.phone
    )
    
    try:
        session.add(master)
        await session.commit()
    except Exception as e:
        return {"ok": False, "message":"Ошибка при добавлении нового мастера"}
    return {"ok": True, "message":"Мастер успешно добавлен"}