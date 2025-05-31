from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from dto.service_schema import ServiceCreate, ServiceGet, ServiceUpdate
from models.service_model import ServiceModel
from .utility import get_object_by_id

async def create_service(service_data: ServiceCreate, session: AsyncSession) -> dict:
    svc = ServiceModel(**service_data.model_dump())
    try:
        session.add(svc)
        await session.commit()
        await session.refresh(svc)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при добавлении услуги", "details": str(e)}
    return {"ok": True, "service_id": svc.id}

async def update_service(service_id: int, data: ServiceUpdate, session: AsyncSession) -> dict:
    svc = await get_object_by_id(ServiceModel, service_id, session)
    if not svc:
        return {"ok": False, "message": "Услуга не найдена"}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(svc, field, value)
    try:
        await session.commit()
        await session.refresh(svc)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при обновлении услуги", "details": str(e)}
    return {"ok": True, "service_id": svc.id}

async def get_service_by_id(service_id: int, session: AsyncSession) -> dict:
    svc = await get_object_by_id(ServiceModel, service_id, session)
    if not svc:
        return {"ok": False, "message": "Услуга не найдена"}
    return {"ok": True, "service": ServiceGet.model_validate(svc)}

async def get_all_services(session: AsyncSession) -> list[ServiceGet]:
    result = await session.execute(select(ServiceModel))
    svcs = result.scalars().all()
    return [ServiceGet.model_validate(s) for s in svcs]

async def delete_service(service_id: int, session: AsyncSession) -> dict:
    svc = await get_object_by_id(ServiceModel, service_id, session)
    if not svc:
        return {"ok": False, "message": "Услуга не найдена"}
    try:
        await session.delete(svc)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при удалении услуги", "details": str(e)}
    return {"ok": True, "message": "Услуга удалена"}