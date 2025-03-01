from sqlalchemy.ext.asyncio import AsyncSession
from schema.request_schema import RequestSchemaCreate
from models.request_model import RequestModel

async def _create_request(RequestInfo: RequestSchemaCreate,session: AsyncSession):
    req = RequestModel(**RequestInfo.__dict__)
    try:
        session.add(req)
        await session.commit()
    except Exception as e:
        return {"ok": False, "message": f"Ошибка при добавлении записи: {e}"}
    return {"ok":True, "message": "Заявка успешно добавлена" }