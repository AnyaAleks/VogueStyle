from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from dto.request_schema import RequestCreate, RequestGet, RequestUpdate
from models.request_model import RequestModel
from .utility import get_object_by_id

async def create_request(request_data: RequestCreate, session: AsyncSession) -> dict:
    req = RequestModel(**request_data.model_dump())
    try:
        session.add(req)
        await session.commit()
        await session.refresh(req)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при создании запроса", "details": str(e)}
    return {"ok": True, "request_id": req.id}

async def update_request(request_id: int, data: RequestUpdate, session: AsyncSession) -> dict:
    req = await get_object_by_id(RequestModel, request_id, session)
    if not req:
        return {"ok": False, "message": "Запрос не найден"}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(req, field, value)
    try:
        await session.commit()
        await session.refresh(req)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при обновлении запроса", "details": str(e)}
    return {"ok": True, "request_id": req.id}

async def get_request_by_id(request_id: int, session: AsyncSession) -> dict:
    result = await session.execute(select(RequestModel).options(
        joinedload(RequestModel.master),
        joinedload(RequestModel.service),
        joinedload(RequestModel.user)
    ).where(RequestModel.id == request_id))
    req: RequestModel | None = result.unique().scalar_one_or_none()
    if not req:
        return {"ok": False, "message": "Запрос не найден"}
    return {"ok": True, "request": RequestGet.model_validate(req)}

async def get_all_requests(session: AsyncSession) -> list[RequestGet]:
    result = await session.execute(select(RequestModel).options(
        joinedload(RequestModel.master),
        joinedload(RequestModel.service),
        joinedload(RequestModel.user)
    ))
    reqs = result.unique().scalars().all()
    return [RequestGet.model_validate(r) for r in reqs]

async def get_all_actual_requests(session: AsyncSession) -> list[RequestGet]:
    result = await session.execute(select(RequestModel).where(RequestModel.schedule_at >= datetime.today()).options(
        joinedload(RequestModel.master),
        joinedload(RequestModel.service),
        joinedload(RequestModel.user)
    ))
    reqs = result.unique().scalars().all()
    return [RequestGet.model_validate(r) for r in reqs]

async def delete_request(request_id: int, session: AsyncSession) -> dict:
    req = await get_object_by_id(RequestModel, request_id, session)
    if not req:
        return {"ok": False, "message": "Запрос не найден"}
    try:
        await session.delete(req)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при удалении запроса", "details": str(e)}
    return {"ok": True, "message": "Запрос удалён"}
