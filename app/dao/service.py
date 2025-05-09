from sqlalchemy.ext.asyncio import AsyncSession
from dto.service_schema import ServiceSchemaGet, ServiceSchemaCreate, ServiceSchemaUpdate
from models.service_model import ServiceModel
from sqlalchemy import select, update

async def _create_service(ServiceInfo: ServiceSchemaCreate,session: AsyncSession):
    req = ServiceModel(**ServiceInfo.__dict__)
    try:
        session.add(req)
        await session.commit()
    except Exception as e:
        return {"ok": False, "message": f"Ошибка при добавлении услуги: {e}"}
    return {"ok":True, "message": "Услуга успешно добавлена"}

async def _get_service_by_id(service_id: int, session: AsyncSession):
    service = None
    try:
        stmt = select(ServiceModel).where(ServiceModel.id == service_id)
        result = await session.execute(stmt)
        service: ServiceModel = result.scalar_one()
    except Exception as e:
        return {"ok": False, "message": f"Ошибка при попытке получения услуги - {e}"}
    return {"ok": True, "service": ServiceSchemaGet(id=service.id, name=service.name, description=service.description, price=service.price, time_minutes=service.time_minutes)}

async def _get_all_services(session: AsyncSession):
    services = []
    try:
        stmt = select(ServiceModel.id, ServiceModel.name, ServiceModel.description, ServiceModel.price, ServiceModel.time_minutes)
        result = await session.execute(stmt)
        data: list[ServiceModel] = result.all()
        for row in data:
            services.append(ServiceSchemaGet(id=row.id, name=row.name, description=row.description, price=row.price, time_minutes=row.time_minutes))
    except Exception as e:
        return {"ok": False, "message": f"Ошибка при попытке получения всех услуг - {e}"}
    return {"ok": True, "services": services}

async def _update_service(ServiceInfo: ServiceSchemaUpdate, session: AsyncSession):
    try:
        await session.execute(update(ServiceModel), [{"id": ServiceInfo.id, "name": ServiceInfo.name, "description": ServiceInfo.description, "price": ServiceInfo.price, "time_minutes": ServiceInfo.time_minutes}])
        await session.commit()
    except Exception as e:
        return {"ok": False, "message": f"При попытке обновления данных услуги была произведена ошибка - {e}"}
    return {"ok": True, "message": "Услуга была успешно обновлена"}