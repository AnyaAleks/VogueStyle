from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import select, insert
from sqlalchemy.orm import joinedload
from dto.service_schema import ServiceCreate, ServiceGet, ServiceUpdate, MasterServiceGet
from dto.servicemaster_schema import ServiceMasterLink
from models.service_model import ServiceModel
from models.master_model import MasterModel
from models.servicemaster_model import services_masters
from .utility import get_object_by_id

async def link_servicemaster(data: ServiceMasterLink, session: AsyncSession) -> dict:
    try:
        master_exists = await session.execute(
            select(MasterModel.id).where(MasterModel.id == data.master_id)
        )
        if master_exists.scalar_one_or_none() is None:
            return {"ok": False, "message": f"Мастер с id={data.master_id} не найден."}
        
        service_exists = await session.execute(
            select(ServiceModel.id).where(ServiceModel.id == data.service_id)
        )
        if service_exists.scalar_one_or_none() is None:
            return {"ok": False, "message": f"Услуга с id={data.service_id} не найдена."}
        
        stmt = (
            insert(services_masters)
            .values(master_id=data.master_id, service_id=data.service_id)
        )
        await session.execute(stmt)
        await session.commit()
        return {
            "ok": True,
            "message": "Связь мастер ↔ услуга успешно создана.",
            "link": {"master_id": data.master_id, "service_id": data.service_id}
        }
    except IntegrityError as e:
        await session.rollback()
        
        return {
            "ok": False,
            "message": f"Невозможно создать связь (возможно, такого мастера или услуги нет, "
                       f"или связь уже существует). Детали ошибки: {e.orig}"
        }

    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": f"Непредвиденная ошибка БД: {e}"}

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
                                           joinedload(ServiceModel.masters)
                                           ))
        svc: ServiceModel | None = result.unique().scalar_one_or_none()
        master_list = [
                MasterServiceGet.model_validate(master, from_attributes=True)
                for master in svc.masters
            ]
        service_schema: ServiceGet = ServiceGet(
            id=svc.id,
            name=svc.name,
            masters=master_list,
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
                                       joinedload(ServiceModel.masters)
                                       ))
    svcs = result.unique().scalars().all()
    output = []
    for svc in svcs:
        master_list = [
                MasterServiceGet.model_validate(master, from_attributes=True)
                for master in svc.masters
            ]
        service_schema: ServiceGet = ServiceGet(
            id=svc.id,
            name=svc.name,
            masters=master_list,
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