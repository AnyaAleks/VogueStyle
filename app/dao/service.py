from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from dto.service_schema import ServiceCreate, ServiceGet, ServiceUpdate, MasterServiceGet
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
    try:
        result = await session.execute(select(ServiceModel)
                                       .where(ServiceModel.id == service_id)
                                       .options(
                                           joinedload(ServiceModel.master)
                                           ))
        svc: ServiceModel | None = result.scalar_one_or_none()
        master_schema: MasterServiceGet = MasterServiceGet.model_validate(svc.master)
        service_schema: ServiceGet = ServiceGet(
            id=svc.id,
            name=svc.name,
            master=master_schema,
            description=svc.description,
            price=svc.price,
            time_minutes=svc.time_minutes
        )
        if not svc:
            return {"ok": False, "message": "Услуга не найдена"}
        return {"ok": True, "service": service_schema}
    except SQLAlchemyError as e:
        return {"ok": False, "message": f"Ошибка при попытке получения услуги: {e}"}

async def get_all_services(session: AsyncSession) -> dict:
    result = await session.execute(select(ServiceModel)
                                   .options(
                                       joinedload(ServiceModel.master)
                                       ))
    svcs = result.scalars().all()
    output = []
    for svc in svcs:
        master_schema: MasterServiceGet = MasterServiceGet.model_validate(svc.master)
        service_schema: ServiceGet = ServiceGet(
            id=svc.id,
            name=svc.name,
            master=master_schema,
            description=svc.description,
            price=svc.price,
            time_minutes=svc.time_minutes
        )
        output.append(service_schema)
    return {"ok": True, "services": output}

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