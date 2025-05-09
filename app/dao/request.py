from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from dto.request_schema import RequestSchemaCreate, RequestSchemaGet
from dto.master_schema import MasterSchemaGet
from dto.service_schema import ServiceSchemaGet
from dto.user_schema import UserSchemaGet
from models.request_model import RequestModel
from dao.user import _get_user_by_id
from dao.master import _get_master_by_id
from dao.service import _get_service_by_id

async def _create_request(RequestInfo: RequestSchemaCreate,session: AsyncSession):
    req = RequestModel(**RequestInfo.__dict__)
    try:
        session.add(req)
        await session.commit()
    except Exception as e:
        return {"ok": False, "message": f"Ошибка при добавлении записи: {e}"}
    return {"ok":True, "message": "Заявка успешно добавлена" }

async def _get_request_by_id(request_id: int, session: AsyncSession):
    request = None
    master = None
    user = None
    service = None
    try:
        stmt = select(RequestModel).where(RequestModel.id == request_id)
        result = await session.execute(stmt)
        request: RequestModel = result.scalar_one()
    except Exception as e: 
        return {"ok": False, "message": f"Ошибка при попытке получения записи - {e}"}
    try:
        pre_master_data = await _get_master_by_id(request.master_id, session)
        master: MasterSchemaGet = pre_master_data["master"]
        pre_user_data = await _get_user_by_id(request.user_id, session)
        user: UserSchemaGet = pre_user_data["user"]
        pre_service_data = await _get_service_by_id(request.service_id, session)
        service: ServiceSchemaGet = pre_service_data["service"]
    except Exception as e:
        return {"ok": False, "message":f"При попытке получения данных для записи - {e}"}
    return {"ok": True, "request": RequestSchemaGet(id=request.id, user=user, master=master, service=service, datetime=request.datetime)}

async def _get_all_actual_requests(session: AsyncSession):
    requests = []
    
    try:
        stmt = select(RequestModel.id, RequestModel.master_id, RequestModel.user_id, RequestModel.service_id, RequestModel.datetime).where(RequestModel.datetime > datetime.now())
        result = await session.execute(stmt)
        data: list[RequestModel] = result.all()
        
        for row in data:
            pre_master_data = await _get_master_by_id(row.master_id, session)
            master: MasterSchemaGet = pre_master_data["master"]
            pre_user_data = await _get_user_by_id(row.user_id, session)
            user: UserSchemaGet = pre_user_data["user"]
            pre_service_data = await _get_service_by_id(row.service_id, session)
            service: ServiceSchemaGet = pre_service_data["service"]
            requests.append(RequestSchemaGet(id=row.id, user=user, service=service, master=master, datetime=row.datetime))
    except Exception as e:
        return {"ok": False, "message": f"Ошибка при попытке получения всех услуг - {e}"}
    return {"ok": True, "requests": requests}

async def _get_all_requests(session: AsyncSession):
    requests = []
    try:
        stmt = select(RequestModel.id, RequestModel.master_id, RequestModel.user_id, RequestModel.service_id, RequestModel.datetime)
        result = await session.execute(stmt)
        data: list[RequestModel] = result.all()
        for row in data:
            pre_master_data = await _get_master_by_id(row.master_id, session)
            master: MasterSchemaGet = pre_master_data["master"]
            pre_user_data = await _get_user_by_id(row.user_id, session)
            user: UserSchemaGet = pre_user_data["user"]
            pre_service_data = await _get_service_by_id(row.service_id, session)
            service: ServiceSchemaGet = pre_service_data["service"]
            requests.append(RequestSchemaGet(id=row.id, user=user, service=service, master=master, datetime=row.datetime))
    except Exception as e:
        return {"ok": False, "message": f"Ошибка при попытке получения всех услуг - {e}"}
    return {"ok": True, "requests": requests}