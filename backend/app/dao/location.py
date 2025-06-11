from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from models.location_model import LocationModel
from models.master_model import MasterModel
from dto.master_schema import MasterGet
from dto.location_schema import LocationCreate, LocationGet, LocationUpdate
from .utility import get_object_by_id

async def create_location(location_data: LocationCreate, session: AsyncSession) -> dict:
    loc = LocationModel(**location_data.model_dump())
    try:
        session.add(loc)
        await session.commit()
        await session.refresh(loc)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при добавлении локации", "details": str(e)}
    return {"ok": True, "location_id": loc.id}

async def update_location(location_id: int, data: LocationUpdate, session: AsyncSession) -> dict:
    loc = await get_object_by_id(LocationModel, location_id, session)
    if not loc:
        return {"ok": False, "message": "Локация не найдена"}
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(loc, field, value)
    try:
        await session.commit()
        await session.refresh(loc)
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при обновлении локации", "details": str(e)}
    return {"ok": True, "location_id": loc.id}

async def get_location_by_id(location_id: int, session: AsyncSession) -> dict:
    loc = await get_object_by_id(LocationModel, location_id, session)
    if not loc:
        return {"ok": False, "message": "Локация не найдена"}

    # Подгружаем связанных мастеров, чтобы loc.masters был списком MasterModel
    await session.refresh(loc, attribute_names=["masters"])
    # Составляем список ID мастеров
    master_ids: List[int] = [m.id for m in loc.masters]

    # Формируем словарь для Pydantic
    data = {
        "id": loc.id,
        "name": loc.name,
        "address": loc.address,
        "masters": master_ids
    }
    return {"ok": True, "location": LocationGet.model_validate(data)}

async def get_masters_by_location_id(location_id: int, session: AsyncSession) -> list[MasterGet]:
    """
    Получить всех мастеров, относящихся к данной локации по её ID.
    """
    result = await session.execute(
        select(MasterModel).where(MasterModel.location_id == location_id)
    )
    masters = result.scalars().all()
    return [MasterGet.model_validate(m) for m in masters]

async def get_all_locations(session: AsyncSession) -> List[LocationGet]:
    # Используем selectinload, чтобы сразу подтянуть всех мастеров для каждой локации
    result = await session.execute(
        select(LocationModel).options(joinedload(LocationModel.masters))
    )
    locs: List[LocationModel] = result.unique().scalars().all()

    output: List[LocationGet] = []
    for loc in locs:
        # Список ID мастеров для текущей локации
        master_ids: List[int] = [m.id for m in loc.masters]

        # Формируем словарь для Pydantic
        data = {
            "id": loc.id,
            "name": loc.name,
            "address": loc.address,
            "masters": master_ids
        }
        output.append(LocationGet.model_validate(data))

    return output

async def delete_location(location_id: int, session: AsyncSession) -> dict:
    loc = await get_object_by_id(LocationModel, location_id, session)
    if not loc:
        return {"ok": False, "message": "Локация не найдена"}
    try:
        await session.delete(loc)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        return {"ok": False, "message": "Ошибка при удалении локации", "details": str(e)}
    return {"ok": True, "message": "Локация удалена"}
